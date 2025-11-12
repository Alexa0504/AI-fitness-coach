from datetime import datetime, date, timedelta
from flask import Blueprint, request, jsonify
from backend.models import db, Goal, UserGoal
from backend.utils.auth_decorator import token_required
from sqlalchemy import extract

goals_bp = Blueprint('goals', __name__, url_prefix='/api/goals')


@goals_bp.route('/', methods=['GET'])
@token_required
def get_goals(current_user):
    """Returns all long-term goals for the user."""
    goals = Goal.query.filter_by(user_id=current_user.id).all()
    return jsonify([g.to_dict() for g in goals]), 200


@goals_bp.route('/', methods=['POST'])
@token_required
def create_goal(current_user):
    """Creates a new long-term goal (e.g., reaching 75 kg)."""
    data = request.get_json()

    goal_type = data.get("goal_type")
    target_value = data.get("target_value")
    unit = data.get("unit")

    if not goal_type:
        return jsonify({"message": "goal_type is required"}), 400

    try:
        goal = Goal(
            user_id=current_user.id,
            goal_type=goal_type,
            target_value=target_value,
            unit=unit
        )
        db.session.add(goal)
        db.session.commit()
        return jsonify({"message": "Goal created", "goal": goal.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        print(f"Error creating long-term goal: {e}")
        return jsonify({"message": "Error creating goal"}), 500


@goals_bp.route('/<int:goal_id>', methods=['PUT'])
@token_required
def update_goal(current_user, goal_id):
    """Updates an existing long-term goal."""
    data = request.get_json()
    goal = Goal.query.filter_by(id=goal_id, user_id=current_user.id).first()

    if not goal:
        return jsonify({"message": "Goal not found"}), 404

    goal.goal_type = data.get("goal_type", goal.goal_type)
    goal.target_value = data.get("target_value", goal.target_value)
    goal.unit = data.get("unit", goal.unit)

    try:
        db.session.commit()
        return jsonify({"message": "Goal updated successfully", "goal": goal.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error updating goal: {e}")
        return jsonify({"message": "Error updating goal"}), 500


@goals_bp.route('/<int:goal_id>', methods=['DELETE'])
@token_required
def delete_goal(current_user, goal_id):
    """Deletes a long-term goal."""
    goal = Goal.query.filter_by(id=goal_id, user_id=current_user.id).first()

    if not goal:
        return jsonify({"message": "Goal not found"}), 404

    try:
        db.session.delete(goal)
        db.session.commit()
        return jsonify({"message": "Goal deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting goal: {e}")
        return jsonify({"message": "Error deleting goal"}), 500


def get_current_week_start():
    """Returns the current Monday's date (ISO standard)."""
    today = date.today()

    start_of_week = today - timedelta(days=today.weekday())
    return start_of_week


@goals_bp.route('/weekly', methods=['GET'])
@token_required
def get_weekly_goals(current_user):
    """Returns the user's weekly goals (starting from the current Monday)."""
    week_start = get_current_week_start()

    weekly_goals = UserGoal.query.filter(
        UserGoal.user_id == current_user.id,
        UserGoal.week_start == week_start
    ).all()

    return jsonify([g.to_dict() for g in weekly_goals]), 200


@goals_bp.route('/weekly', methods=['POST'])
@token_required
def create_weekly_goal(current_user):
    """Creates a new weekly goal (e.g., 3x workout this week)."""
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


@goals_bp.route('/weekly/<int:goal_id>/toggle', methods=['PATCH'])
@token_required
def toggle_weekly_goal(current_user, goal_id):
    """Toggles the 'is_completed' status of a weekly goal."""
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
