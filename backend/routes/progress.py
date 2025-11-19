from flask import Blueprint, request, jsonify
from datetime import datetime
from backend.models import db, User
from backend.utils.auth_decorator import token_required

progress_bp = Blueprint("progress", __name__, url_prefix="/api/progress")

@progress_bp.route("/save", methods=["PATCH"])
@token_required
def save_progress(current_user):
    data = request.get_json() or {}

    if "progress" not in data:
        return jsonify({"message": "Missing progress object"}), 400

    progress = data["progress"]

    current_user.set_progress(progress)
    current_user.last_progress_update = datetime.utcnow()

    db.session.commit()

    return jsonify({
        "message": "Progress saved",
        "progress": current_user.get_progress(),
        "last_progress_update": current_user.last_progress_update.isoformat()
    }), 200
