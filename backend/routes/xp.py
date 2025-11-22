from flask import Blueprint, jsonify, request
from backend.utils.auth_decorator import token_required
from backend.services.xp_service import update_weekly_xp, get_xp_status
from flask_cors import cross_origin

xp_bp = Blueprint("xp", __name__, url_prefix="/api/xp")


@xp_bp.route("/update", methods=["POST", "OPTIONS"])
@cross_origin()
@token_required
def xp_update(current_user):

    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    success, message = update_weekly_xp(current_user)
    return jsonify({"success": success, "message": message}), (200 if success else 400)


@xp_bp.route("/status", methods=["GET", "OPTIONS"])
@cross_origin()
@token_required
def xp_status(current_user):

    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    return jsonify(get_xp_status(current_user)), 200
