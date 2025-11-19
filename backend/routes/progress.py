from flask import Blueprint, request, jsonify
from backend.utils.auth_decorator import token_required
from backend.models import db
from datetime import datetime, timezone

progress_bp = Blueprint("progress", __name__, url_prefix="/api/progress")


@progress_bp.route("/save", methods=["PATCH"])
@token_required
def save_progress(current_user):
    """Saves workout/diet progress for the user."""
    data = request.get_json()

    if not data:
        return jsonify({"message": "No progress data sent"}), 400

    try:
        current_user.set_progress_state(data)
        current_user.last_progress_update = datetime.now(timezone.utc)

        db.session.commit()

        return jsonify({
            "message": "Progress saved successfully",
            "progress": current_user.get_progress_state(),
            "last_update": current_user.last_progress_update.isoformat()
        }), 200

    except Exception as e:
        print("Progress save error:", e)
        db.session.rollback()
        return jsonify({"message": "Error saving progress"}), 500
