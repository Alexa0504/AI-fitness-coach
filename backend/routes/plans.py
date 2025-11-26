import json
from flask import Blueprint, request, jsonify
from backend.models import db, Plan
from backend.utils.mock_data import get_mock_plan
from backend.utils.auth_decorator import token_required
from backend.utils.score_utils import calculate_mock_score
from backend.utils.ai_integration import generate_plan, get_mock_user_data
from datetime import date, datetime
from sqlalchemy import desc
from backend.services.xp_service import update_weekly_xp, get_xp_status

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

        content_dict = json.loads(content_string)

        
        if plan_type == "workout":
            for day in content_dict.get("days", []):
                day["completed"] = False
        elif plan_type == "diet":
            for meal_day in content_dict.get("meals", []):
                meal_day["breakfast_completed"] = False
                meal_day["lunch_completed"] = False
                meal_day["dinner_completed"] = False

        content_string = json.dumps(content_dict)
        score = calculate_mock_score(plan_type)


        new_plan = Plan(
            user_id=current_user.id,
            plan_type=plan_type,
            content=content_string,
            score=score,
            start_date=plan_start_date or datetime.utcnow()
        )
        db.session.add(new_plan)
        db.session.commit()

        user_plans = Plan.query.filter_by(user_id=current_user.id).all()
        return jsonify({
            "message": "New plan created successfully",
            "plan": _plan_to_response(new_plan),
            "plans": [_plan_to_response(p) for p in user_plans]
        }), 201

    except Exception as e:
        db.session.rollback()
        print(f"Error creating plan: {e}")
        return jsonify({"message": "Error creating plan"}), 500


@plans_bp.route('/<int:plan_id>', methods=['PUT', 'PATCH'])
@token_required
def update_plan(plan_id, current_user):
    data = request.get_json() or {}
    plan = Plan.query.filter_by(id=plan_id, user_id=current_user.id).first()
    if not plan:
        return jsonify({"message": "Plan not found"}), 404

    if "start_date" in data:
        try:
            plan.start_date = date.fromisoformat(data["start_date"])
        except ValueError:
            return jsonify({"message": "Invalid start_date format. Use YYYY-MM-DD."}), 400

    if "content" in data:
        new_content = data["content"]
        plan.content = json.dumps(new_content) if isinstance(new_content, (dict, list)) else new_content

    if "plan_type" in data and data["plan_type"] != plan.plan_type:
        plan.plan_type = data["plan_type"]
        plan.score = calculate_mock_score(plan.plan_type)
    elif "score" in data:
        plan.score = data["score"]

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
            target = next((d for d in content.get("days", []) if int(d.get("day")) == day), None)
            if not target:
                return jsonify({"message": "Day not found"}), 404
            target[field] = True

        elif t == "diet_meal":
            day = int(payload.get("day"))
            meal = payload.get("meal")
            target = next((m for m in content.get("meals", []) if int(m.get("day")) == day), None)
            if not target:
                return jsonify({"message": "Day not found"}), 404
            target[f"{meal}_completed"] = True
        else:
            return jsonify({"message": "Unsupported toggle type"}), 400

        plan.content = json.dumps(content)
        update_weekly_xp(current_user)
        db.session.commit()
        xp_data = get_xp_status(current_user)

        return jsonify({
            "message": "Toggle saved",
            "plan": _plan_to_response(plan),
            "xp": xp_data
        }), 200

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
