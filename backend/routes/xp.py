from flask import Blueprint, jsonify
from backend.utils.auth_decorator import token_required
from backend.services.xp_service import update_weekly_xp, get_xp_status

xp_bp = Blueprint("xp", __name__, url_prefix="/api/xp")


@xp_bp.route("/update", methods=["POST"])
@token_required
def xp_update(current_user):
    success, message = update_weekly_xp(current_user)
    return jsonify({"success": success, "message": message}), (200 if success else 400)


@xp_bp.route("/status", methods=["GET"])
@token_required
def xp_status(current_user):
    return jsonify(get_xp_status(current_user)), 200
