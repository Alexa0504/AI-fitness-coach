from flask import Blueprint, jsonify
from backend.services.performance_service import PerformanceService
from backend.utils.auth_decorator import token_required

stats_bp = Blueprint("stats", __name__, url_prefix="/user/stats")

@stats_bp.route("/", methods=["GET"])
@token_required
def get_user_stats(current_user):
    performance = PerformanceService.calculate_weekly_performance(current_user.id)
    return jsonify({"performance_percentage": performance}), 200
