from flask import Blueprint, request, jsonify
from backend.models import db, Plan
from backend.utils.mock_data import get_mock_plan
from backend.utils.auth_decorator import token_required
from backend.utils.score_utils import calculate_mock_score
from backend.utils.ai_integration import generate_plan, get_mock_user_data

plans_bp = Blueprint('plans', __name__, url_prefix='/api/plans')


@plans_bp.route('/', methods=['GET'])
@token_required
def get_user_plans(current_user):
    """Get all plans for the current user"""
    user_plans = Plan.query.filter_by(user_id=current_user.id).all()
    return jsonify([plan.to_dict() for plan in user_plans]), 200


@plans_bp.route('/<int:plan_id>', methods=['GET'])
@token_required
def get_single_plan(plan_id, current_user):
    """Get a specific plan by ID for the current user"""
    plan = Plan.query.filter_by(id=plan_id, user_id=current_user.id).first()
    if not plan:
        return jsonify({"message": "Plan not found"}), 404
    return jsonify(plan.to_dict()), 200


@plans_bp.route('/', methods=['POST'])
@token_required
def create_plan(current_user):
    """Create a new AI-generated plan (mocked for now)"""
    data = request.get_json()
    plan_type = data.get("plan_type", "workout")

    try:
        user_data = get_mock_user_data(current_user.id)

        result = generate_plan(user_data, plan_type)

        if result["error"] or not result["plan_content_string"]:
            return jsonify({
                "message": f"Error generating plan via AI: {result.get('error', 'Unknown error')}"
            }), 500

        content = result["plan_content_string"]

        score = calculate_mock_score(plan_type)

        new_plan = Plan(
            user_id=current_user.id,
            plan_type=plan_type,
            content=content,
            score=score
        )
        db.session.add(new_plan)
        db.session.commit()

        return jsonify({
            "message": "Plan created successfully",
            "plan": new_plan.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        print(f"Error creating plan: {e}")
        return jsonify({"message": "Error creating plan"}), 500


@plans_bp.route('/<int:plan_id>', methods=['PUT'])
@token_required
def update_plan(plan_id, current_user):
    """Update a plan (e.g. update score, content, or plan type)"""
    data = request.get_json()
    plan = Plan.query.filter_by(id=plan_id, user_id=current_user.id).first()

    if not plan:
        return jsonify({"message": "Plan not found"}), 404

    plan.content = data.get("content", plan.content)

    new_plan_type = data.get("plan_type", plan.plan_type)
    if new_plan_type != plan.plan_type:
        plan.plan_type = new_plan_type

        plan.score = calculate_mock_score(plan.plan_type)
    else:

        plan.score = data.get("score", plan.score)

    try:
        db.session.commit()
        return jsonify({
            "message": "Plan updated successfully",
            "plan": plan.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error updating plan: {e}")
        return jsonify({"message": "Error updating plan"}), 500


@plans_bp.route('/<int:plan_id>', methods=['DELETE'])
@token_required
def delete_plan(plan_id, current_user):
    """Delete a plan for the current user"""
    plan = Plan.query.filter_by(id=plan_id, user_id=current_user.id).first()

    if not plan:
        return jsonify({"message": "Plan not found"}), 404

    try:
        db.session.delete(plan)
        db.session.commit()
        return jsonify({"message": "Plan deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting plan: {e}")
        return jsonify({"message": "Error deleting plan"}), 500
