# 添加一条 token 检索路由，以便客户端在需要 token 时调用
from flask import jsonify, g
from flask_vue import db
from flask_vue.api import bp
from flask_vue.api.auth import basic_auth, token_auth

'''
装饰器 @basic_auth.login_required 将指示 Flask-HTTPAuth 验证身份，
当通过 Basic Auth 验证后，才使用用户模型的 get_token() 
方法来生成 token，数据库提交在生成 token 后发出，以确保 token 
及其到期时间被写回到数据库
'''
@bp.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    token = g.current_user.get_token()
    db.session.commit()
    return jsonify(dict(token=token))

@bp.route('/tokens', methods=['DELETE'])
@basic_auth.login_required
def remove_token():
    g.current_user.remove_token()
    db.session.commit()
    return '',204