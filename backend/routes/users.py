from flask import Blueprint, request, jsonify
from backend.models import db, User
from backend.utils.auth_decorator import token_required

users_bp = Blueprint('users', __name__, url_prefix='/api/users')


@users_bp.route('/profile', methods=['GET'])
@token_required
def get_user_profile(current_user):
    """
    Returns the current user's essential profile data.
    """

    return jsonify(current_user.to_dict()), 200


@users_bp.route('/profile', methods=['PUT'])
@token_required
def update_user_profile(current_user):
    """
    Updates the essential physical and goal data (gender, height, weight, target_weight)
    for the current user.
    """
    data = request.get_json() or {}

    try:

        if "gender" in data and data["gender"] is not None:
            gender = data["gender"].lower()
            if gender not in ['male', 'female']:
                return jsonify({"message": "Invalid value for gender. Must be 'male' or 'female'."}), 400
            current_user.gender = gender

        if "height_cm" in data and data["height_cm"] is not None:
            current_user.height_cm = float(data["height_cm"])

        if "weight_kg" in data and data["weight_kg"] is not None:
            current_user.weight_kg = float(data["weight_kg"])

        if "target_weight_kg" in data and data["target_weight_kg"] is not None:
            current_user.target_weight_kg = float(data["target_weight_kg"])

        if "age" in data and data["age"] is not None:
            try:
                current_user.age = int(data["age"])
            except ValueError:
                return jsonify({"message": "Age must be a number."}), 400

        db.session.commit()

        return jsonify({
            "message": "User profile updated successfully",
            "user": current_user.to_dict()
        }), 200

    except ValueError:
        db.session.rollback()
        return jsonify({
            "message": "Invalid format for numeric fields. Expected numbers for height, weight, and target weight."}), 400
    except Exception as e:
        db.session.rollback()
        print(f"Error updating user profile: {e}")
        return jsonify({"message": "Internal error updating profile."}), 500
