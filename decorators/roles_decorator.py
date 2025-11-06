from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask import jsonify

def roles_required(*roles):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            user_role = claims.get("role")
            if user_role in roles:
                return fn(*args, **kwargs)
            return jsonify({"msg": "Permisos insuficientes"}), 403
        return decorator
    return wrapper
