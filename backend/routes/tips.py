# backend/routes/tips.py

from flask import Blueprint, jsonify
from backend.models import Tip
import random

tips_bp = Blueprint('tips', __name__, url_prefix='/tips')

# Ezt a meglévő endpointot cseréld le ezzel:
@tips_bp.route('/<category>/weekly', methods=['GET'])
def get_weekly_tips(category):
    all_tips = Tip.query.filter_by(category=category).all()
    sample_tips = random.sample(all_tips, min(3, len(all_tips))) if all_tips else []
    return jsonify([t.to_dict() for t in sample_tips])