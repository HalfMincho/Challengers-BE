from methods import token
from functools import wraps
from flask import request, jsonify, Response
import base64


def is_api(required_keys=None, acceptable_keys=None, input_type: str = 'query_string'):
    if required_keys is None:
        required_keys = []
    if acceptable_keys is None:
        acceptable_keys = []

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if request.method == "OPTIONS":
                return jsonify({'message': 'preflight_request'}), 200
            if input_type == 'query_string':
                data = request.args
            elif input_type == 'json':
                request.on_json_loading_failed = lambda: jsonify({'error': 'JSON_parsing_failed'}), 400
                data = request.get_json()
                if not isinstance(data, dict):
                    return jsonify({'error': 'dictionary_required'}), 400
            else:
                return jsonify({'error': 'server_side_error_contact_administrator'}), 400

            data = {str(k).lower(): v for k, v in data.items() if k in required_keys or k in acceptable_keys}
            if not set(required_keys).issubset(set(data.keys())):
                return jsonify({'error': 'no_required_args'}), 400
            else:
                return return_api(func, data, *args, **kwargs)

        return wrapper

    return decorator


def return_as_api(function):
    @wraps(function)
    def decorator(*args, **kwargs):
        return return_api(function, *args, **kwargs)

    return decorator


def return_api(func, *args, **kwargs):
    ret_data: Response = func(*args, **kwargs)
    if isinstance(ret_data, tuple):
        if not isinstance(ret_data[0], Response):
            resp = jsonify(ret_data[0])
        else:
            resp = ret_data[0]
        return resp, ret_data[1]
    else:
        if not isinstance(ret_data, Response):
            return jsonify(ret_data)
        else:
            return ret_data


def protected(verify: bool = False):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if 'Authorization' not in request.headers:
                return jsonify({'error': 'no_permission'}), 403
            auth: str = request.headers['Authorization']
            if auth[:5].lower() != 'token':
                return jsonify({'error': 'no_permission'}), 403
            auth = auth.split(' ', 1)[1]
            try:
                if len(base64.b64decode(auth.encode())) != 128:
                    return jsonify({'error': 'no_permission'}), 403
            except:
                return jsonify({'error': 'no_permission'}), 403
            if not token.check(auth):
                return jsonify({'error': 'no_permission'}), 403
            owner = token.get_owner(auth)
            if owner is None:
                return jsonify({'error': 'no_permission'}), 403
            if verify:
                if not token.verify(auth):
                    return jsonify({'error': 'no_permission'}), 403
            return func(True, owner, auth, *args, **kwargs)
        return wrapper
    return decorator


from .challenge import challenge_blueprint
