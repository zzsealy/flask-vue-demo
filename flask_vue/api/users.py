from flask_vue.api import bp
import re
from flask import request, jsonify, url_for
from flask_vue import db
from flask_vue.api import bp
from flask_vue.api.errors import bad_request
from flask_vue.api.auth import token_auth
from flask_vue.models import User

@bp.route('/users', methods=['POST'])
def create_user():
    '''注册一个新用户'''
    data = request.get_json() # 获取前端传过来的数据
    if not data:
        return bad_request("你必须传入JSON数据。")
    message = {}
    if 'username' not in data or not data.get('username', None):
        message['username'] = '请提供用户名！'
    if 'email' not in data or not data.get('email', None):
        message['email'] = '请提供邮箱！'
    if 'password' not in data or not data.get('password', None):
        message['password'] = '请输入密码!'

    if User.query.filter_by(username = data.get('username', None)).first():
        message['username'] = '该用户已存在！' 
    if User.query.filter_by(email = data.get('email', None)).first():
        message['email'] = '邮箱已被注册！'
    if message:
        return bad_request(message)
    
    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())  # 注册完，返回数据。
    response.status_code = 201
    # HTTP协议要求201响应包含一个值为新资源URL的location头部。
    response.headers['location'] = url_for('api.get_user', id=user.id)
    return response


@bp.route('/users', methods=['GET'])
@token_auth.login_required
def get_users():
    '''返回所有用户的集合, 分页'''
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = User.to_collection_dict(User.query, page, per_page, 'api.get_users')
    return jsonify(data)

@bp.route('/users/<int:id>', methods=['GET'])
@token_auth.login_required
def get_user(id):
    '''返回一个用户'''
    return jsonify(User.query.get_or_404(id).to_dict())

@bp.route('/users/<int:id>', methods=['PUT'])
@token_auth.login_required
def update(id):
    '''修改一个用户'''
    user = User.query.get_or_404(id)
    data = request.get_json()
    if not data:
        return bad_request('你必须传入JSON数据')
    message = {}        
    if 'username' in data and not data.get('username', None):
        message['username'] = '请输入有效的用户名!'
    if 'email' in data and not data.get('email', None):
        message['email'] = '请提供有效的邮箱!'
    if 'username' in data and data['username'] != user.username and \
        User.query.filter_by(username=data['username']).first():
        message['username'] = '请提供一个不同的用户名！'
    if 'email' in data and data['email'] != user.email and \
        User.query.filter_by(email=data['email']).first():
        message['email'] = '请提供一个不同的邮箱！'
    
    if message:
        return bad_request(message)
    user.from_dict(data, new_user=False)
    db.session.commit()
    return jsonify(user.to_dict())


@bp.route('/users/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_user(id):
    '''删除一个用户'''
    pass