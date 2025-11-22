from flask import Blueprint, request, jsonify
from backend.utils.auth_decorator import token_required
from backend.models import db
from datetime import datetime, timezone
from flask_cors import cross_origin

progress_bp = Blueprint("progress", __name__, url_prefix="/api/progress")


@progress_bp.route("/save", methods=["PATCH", "OPTIONS"])
@cross_origin()
@token_required
def save_progress(current_user):
    data = request.get_json()

    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

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


@progress_bp.route("/status", methods=["GET", "OPTIONS"])
@cross_origin()
@token_required
def get_progress_status(current_user):

    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    progress = current_user.get_progress_state() or {}

    workout_progress = progress.get("workout", 0)
    diet_progress = progress.get("diet", 0)
    overall = round((workout_progress + diet_progress) / 2) if (workout_progress or diet_progress) else 0

    return jsonify({
        "workoutProgress": workout_progress,
        "dietProgress": diet_progress,
        "overallPerformance": overall,
    }), 200
