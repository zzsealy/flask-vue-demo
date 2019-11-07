from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES
from flask_vue.api import bp
from flask_vue import  db

def error_response(status_code, message=None):
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknow error')}
    if message:
        payload['message'] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response

def bad_request(message):
    '''400错误'''
    return error_response(400, message)

@bp.app_errorhandler(404)
def not_found_error(error):
    return error_response(404)

@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return error_response(500)

