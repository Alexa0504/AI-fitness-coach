from datetime import date, timedelta, datetime
from flask import Blueprint, request, jsonify
from backend.models import db, UserGoal
from backend.utils.auth_decorator import token_required

weekly_goals_bp = Blueprint('weekly_goals', __name__, url_prefix='/api/goals/weekly')


def get_current_week_start():
    """Returns the current Monday's date (ISO standard)."""
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())
    return start_of_week


@weekly_goals_bp.route('/', methods=['GET'])
@token_required
def get_weekly_goals(current_user):
    """Return all weekly goals for the current user starting from this Monday."""
    week_start = get_current_week_start()

    weekly_goals = UserGoal.query.filter_by(user_id=current_user.id, week_start=week_start).all()
    return jsonify([g.to_dict() for g in weekly_goals]), 200


@weekly_goals_bp.route('/', methods=['POST'])
@token_required
def create_weekly_goal(current_user):
    """Create a new weekly goal."""
    data = request.get_json()
    goal_name = data.get("goal_name")

    if not goal_name:
        return jsonify({"message": "goal_name is required"}), 400

    week_start = get_current_week_start()

    try:
        new_goal = UserGoal(
            user_id=current_user.id,
            goal_name=goal_name,
            week_start=week_start,
            is_completed=False
        )
        db.session.add(new_goal)
        db.session.commit()
        return jsonify({"message": "Weekly goal created", "goal": new_goal.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        print(f"Error creating weekly goal: {e}")
        return jsonify({"message": "Error creating weekly goal"}), 500


@weekly_goals_bp.route('/<int:goal_id>/toggle', methods=['PATCH'])
@token_required
def toggle_weekly_goal(current_user, goal_id):
    """Toggle the 'is_completed' status of a weekly goal."""
    goal = UserGoal.query.filter_by(id=goal_id, user_id=current_user.id).first()

    if not goal:
        return jsonify({"message": "Weekly goal not found"}), 404

    try:
        goal.is_completed = not goal.is_completed
        db.session.commit()
        message = "Weekly goal marked as completed." if goal.is_completed else "Weekly goal marked as pending."
        return jsonify({"message": message, "goal": goal.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error toggling weekly goal: {e}")
        return jsonify({"message": "Error toggling weekly goal"}), 500
