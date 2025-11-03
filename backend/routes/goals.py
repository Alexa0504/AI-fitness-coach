from flask import Blueprint, request, jsonify
from backend.models import db, Goal
from backend.utils.auth_decorator import token_required

goals_bp = Blueprint('goals', __name__, url_prefix='/api/goals')


@goals_bp.route('/', methods=['GET'])
@token_required
def get_goals(current_user):
    """Get all goals for the current user"""
    goals = Goal.query.filter_by(user_id=current_user.id).all()
    return jsonify([g.to_dict() for g in goals]), 200


@goals_bp.route('/', methods=['POST'])
@token_required
def create_goal(current_user):
    """Create a new goal for the current user"""
    data = request.get_json()
    goal = Goal(
        user_id=current_user.id,
        goal_type=data.get("goal_type"),
        target_value=data.get("target_value"),
        unit=data.get("unit")
    )
    db.session.add(goal)
    db.session.commit()
    return jsonify({"message": "Goal created", "goal": goal.to_dict()}), 201


@goals_bp.route('/<int:goal_id>', methods=['PUT'])
@token_required
def update_goal(goal_id, current_user):
    """Update an existing goal for the current user"""
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
def delete_goal(goal_id, current_user):
    """Delete a goal for the current user"""
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
