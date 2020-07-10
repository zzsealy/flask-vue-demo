from flask import jsonify
from flask_vue.api import bp

@bp.route('/ping', methods=['GET'])
def ping():
    ''' 用来测试连通性 '''
    return jsonify('Pong!')

