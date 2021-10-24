from flask import jsonify 
from werkzeug.http import HTTP_STATUS_CODES


def error_response(status_codes, message=None):
    """
    use werkzeug's http status codes dictionary for convenience
    """
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}

    if message:
        payload['message'] = message

    response = jsonify(payload)
    response.status_code

    return response 


def bad_request(message):
    """
    most common error is 400, this is a convenience function for that
    """
    return error_response(400, message)
