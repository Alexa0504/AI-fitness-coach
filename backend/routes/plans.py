import json
from flask import Blueprint, request, jsonify
from backend.models import db, Plan
from backend.utils.mock_data import get_mock_plan
from backend.utils.auth_decorator import token_required
from backend.utils.score_utils import calculate_mock_score
from backend.utils.ai_integration import generate_plan, get_mock_user_data
from datetime import date
from sqlalchemy import desc

plans_bp = Blueprint('plans', __name__, url_prefix='/api/plans')


def _parse_plan_content_field(content_field):
    if content_field is None:
        return None
    if isinstance(content_field, (dict, list)):
        return content_field
    try:
        return json.loads(content_field)
    except Exception:
        return content_field


def _plan_to_response(plan):
    p = plan.to_dict()
    p["content"] = _parse_plan_content_field(p.get("content"))
    return p


@plans_bp.route('/latest', methods=['GET'])
@token_required
def get_latest_plans(current_user):
    latest_workout_plan = Plan.query.filter_by(
        user_id=current_user.id,
        plan_type='workout'
    ).order_by(desc(Plan.created_at)).first()

    latest_diet_plan = Plan.query.filter(
        Plan.user_id == current_user.id,
        Plan.plan_type.in_(['diet'])
    ).order_by(desc(Plan.created_at)).first()

    plans_list = []
    if latest_workout_plan:
        plans_list.append(_plan_to_response(latest_workout_plan))
    else:
        plans_list.append(get_mock_plan("workout"))

    if latest_diet_plan:
        plans_list.append(_plan_to_response(latest_diet_plan))
    else:
        plans_list.append(get_mock_plan("diet"))

    return jsonify({"plans": plans_list}), 200


@plans_bp.route('/', methods=['GET'])
@token_required
def get_user_plans(current_user):
    """Return all plans for the current user (parsed content)."""
    user_plans = Plan.query.filter_by(user_id=current_user.id).all()
    return jsonify([_plan_to_response(plan) for plan in user_plans]), 200


@plans_bp.route('/<int:plan_id>', methods=['GET'])
@token_required
def get_single_plan(plan_id, current_user):
    plan = Plan.query.filter_by(id=plan_id, user_id=current_user.id).first()
    if not plan:
        return jsonify({"message": "Plan not found"}), 404
    return jsonify(_plan_to_response(plan)), 200


@plans_bp.route('/', methods=['POST'])
@token_required
def create_plan(current_user):
    """
    Create/update AI-generated plan. Persist per user + plan_type.
    Return both "plan" (the created/updated one) and "plans" (all user plans).
    """
    data = request.get_json() or {}
    plan_type = data.get("plan_type", "workout")

    start_date_str = data.get("start_date")
    plan_start_date = None
    if start_date_str:
        try:

            plan_start_date = date.fromisoformat(start_date_str)
        except ValueError:
            return jsonify({"message": "Invalid start_date format. Use YYYY-MM-DD."}), 400
    try:
        user_data = get_mock_user_data(current_user.id)
        result = generate_plan(user_data, plan_type)

        if not result.get("plan_content_string"):
            return jsonify({"message": f"Error generating plan via AI: {result.get('error', 'Unknown error')}"}), 500

        content_string = result["plan_content_string"]
        if isinstance(content_string, (dict, list)):
            content_string = json.dumps(content_string)

        score = calculate_mock_score(plan_type)

        existing_plan = Plan.query.filter_by(user_id=current_user.id, plan_type=plan_type).first()
        if existing_plan:
            existing_plan.content = content_string
            existing_plan.score = score
            if plan_start_date:
                existing_plan.start_date = plan_start_date
            db.session.commit()
            plan_obj = existing_plan
            status_code = 200
            message = "Plan updated successfully"
        else:
            new_plan = Plan(user_id=current_user.id, plan_type=plan_type, content=content_string, score=score)
            db.session.add(new_plan)
            db.session.commit()
            plan_obj = new_plan
            status_code = 201
            message = "Plan created successfully"

        user_plans = Plan.query.filter_by(user_id=current_user.id).all()
        return jsonify({
            "message": message,
            "plan": _plan_to_response(plan_obj),
            "plans": [_plan_to_response(p) for p in user_plans]
        }), status_code

    except Exception as e:
        db.session.rollback()
        print(f"Error creating plan: {e}")
        return jsonify({"message": "Error creating plan"}), 500


@plans_bp.route('/<int:plan_id>', methods=['PUT', 'PATCH'])
@token_required
def update_plan(plan_id, current_user):
    """Update content/score/plan_type. Accepts content dict or JSON-string."""
    data = request.get_json() or {}
    plan = Plan.query.filter_by(id=plan_id, user_id=current_user.id).first()
    if not plan:
        return jsonify({"message": "Plan not found"}), 404

    if "start_date" in data:
        start_date_str = data["start_date"]
        try:
            plan.start_date = date.fromisoformat(start_date_str)
        except ValueError:
            return jsonify({"message": "Invalid start_date format. Use YYYY-MM-DD."}), 400

    if "content" in data:
        new_content = data["content"]
        plan.content = json.dumps(new_content) if isinstance(new_content, (dict, list)) else new_content

    new_plan_type = data.get("plan_type")
    if new_plan_type and new_plan_type != plan.plan_type:
        plan.plan_type = new_plan_type
        plan.score = calculate_mock_score(plan.plan_type)
    else:
        if "score" in data:
            plan.score = data.get("score")

    try:
        db.session.commit()
        return jsonify({"message": "Plan updated successfully", "plan": _plan_to_response(plan)}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error updating plan: {e}")
        return jsonify({"message": "Error updating plan"}), 500


@plans_bp.route('/<int:plan_id>/toggle', methods=['PATCH'])
@token_required
def toggle_checkbox(plan_id, current_user):
    """
    Toggle checkbox for workout day or diet meal.
    """
    payload = request.get_json() or {}
    plan = Plan.query.filter_by(id=plan_id, user_id=current_user.id).first()
    if not plan:
        return jsonify({"message": "Plan not found"}), 404

    content = _parse_plan_content_field(plan.content)
    if not isinstance(content, dict):
        return jsonify({"message": "Plan content invalid JSON"}), 400

    try:
        t = payload.get("type")
        if t == "workout_day":
            day = int(payload.get("day"))
            field = payload.get("field", "completed")
            value = bool(payload.get("value", True))
            days = content.get("days", [])
            target = next((d for d in days if int(d.get("day")) == day), None)
            if not target:
                return jsonify({"message": "Day not found"}), 404
            target[field] = value

        elif t == "diet_meal":
            day = int(payload.get("day"))
            meal = payload.get("meal")
            value = bool(payload.get("value", True))
            meals = content.get("meals", [])
            target = next((m for m in meals if int(m.get("day")) == day), None)
            if not target:
                return jsonify({"message": "Day not found"}), 404
            key = f"{meal}_completed"  # Ezt a kulcsot várja a Taskbar a frontendben!
            target[key] = value

        else:
            return jsonify({"message": "Unsupported toggle type"}), 400

        plan.content = json.dumps(content)
        db.session.commit()
        return jsonify({"message": "Toggle saved", "plan": _plan_to_response(plan)}), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error toggling checkbox: {e}")
        return jsonify({"message": "Error toggling checkbox"}), 500


@plans_bp.route('/<int:plan_id>', methods=['DELETE'])
@token_required
def delete_plan(plan_id, current_user):
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