from functools import wraps
from flask import request, jsonify
from backend.models import User
from backend.utils.security_utils import decode_auth_token
from backend.utils.token_blacklist import is_token_blacklisted


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        # Allow CORS preflight requests to go through without token
        if request.method == "OPTIONS":
            return jsonify({"status": "ok"}), 200

        token = None

        # Extract token
        if "Authorization" in request.headers:
            parts = request.headers["Authorization"].split(" ")
            if len(parts) == 2:
                token = parts[1]

        if not token:
            return jsonify({"message": "Token is missing!"}), 401

        if is_token_blacklisted(token):
            return jsonify({"message": "Token has been revoked. Please log in again."}), 401

        user_id = decode_auth_token(token)

        if not user_id:
            return jsonify({"message": "Token is invalid or expired!"}), 401

        user = User.query.get(user_id)
        if not user:
            return jsonify({"message": "User not found!"}), 404

        return f(current_user=user, *args, **kwargs)

    return decorated
