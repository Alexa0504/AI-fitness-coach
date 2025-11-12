from flask import Blueprint, request, jsonify
from backend.models import db, UserGoal
from backend.utils.auth_decorator import token_required

weekly_bp = Blueprint("weekly_goals", __name__, url_prefix="/api/weekly-goals")

@weekly_bp.route("/", methods=["GET"])
@token_required
def get_weekly_goals(current_user):
    weekly_goals = UserGoal.query.filter_by(user_id=current_user.id).all()
    return jsonify([g.to_dict() for g in weekly_goals]), 200

@weekly_bp.route("/<int:goal_id>/toggle/<string:day>", methods=["PATCH"])
@token_required
def toggle_daily_goal(current_user, goal_id, day):
    goal = UserGoal.query.filter_by(id=goal_id, user_id=current_user.id).first()
    if not goal:
        return jsonify({"message": "Weekly goal not found"}), 404

    if day not in ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]:
        return jsonify({"message": "Invalid day"}), 400

    try:
        current_status = getattr(goal, day)
        setattr(goal, day, not current_status)
        db.session.commit()
        return jsonify({"goal": goal.to_dict(), "progress": goal.progress}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error toggling daily goal"}), 500
