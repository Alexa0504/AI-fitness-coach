from flask import Blueprint, jsonify
from backend.models import Tip
import random

tips_bp = Blueprint('tips', __name__, url_prefix='/tips')

@tips_bp.route('/general/weekly', methods=['GET'])
def get_weekly_tips():
    all_tips = Tip.query.filter_by(category='general').all()
    sample_tips = random.sample(all_tips, min(3, len(all_tips)))
    return jsonify([t.to_dict() for t in sample_tips])
