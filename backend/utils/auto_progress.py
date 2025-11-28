from backend.models import db
from datetime import datetime, timezone
import json


def auto_save_progress(user, progress_obj):
    progress_json_string = json.dumps(progress_obj)

    user.set_progress_state(progress_json_string)

    user.last_progress_update = datetime.now(timezone.utc)
    db.session.commit()
