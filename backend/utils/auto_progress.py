from backend.models import db
from datetime import datetime, timezone

def auto_save_progress(user, progress_obj):
    user.set_progress_state(progress_obj)
    user.last_progress_update = datetime.now(timezone.utc)
    db.session.commit()
