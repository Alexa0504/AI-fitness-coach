from flask import Blueprint, request, jsonify
from backend.utils.auth_decorator import token_required
from backend.services.xp_service import add_xp, xp_status, WEEKLY_GOAL_XP

xp_bp = Blueprint("xp", __name__, url_prefix="/api/xp")

@xp_bp.route("/update", methods=["POST"])
@token_required
def update_xp(current_user):
    data = request.get_json() or {}
    amount = data.get("amount")

    if amount is None:
        return jsonify({"message": "Missing XP amount"}), 400

    result = add_xp(current_user, int(amount))
    return jsonify(result), 200


@xp_bp.route("/status", methods=["GET"])
@token_required
def get_status(current_user):
    return jsonify(xp_status(current_user)), 200
