from backend.models import db
from datetime import datetime, timezone
import json  # Ezt az importot hozzá kell adnod


# Tegyük fel, hogy a user.set_progress_state() metódus a progress_saved_state
# attribútumot állítja be.

def auto_save_progress(user, progress_obj):
    # 1. Alakítsd át a szótárat JSON stringgé
    progress_json_string = json.dumps(progress_obj)

    # 2. Add át a stringet a modelnek (attól függően, hogy a set_progress_state mit csinál):

    # Ha a set_progress_state csak beállítja az attribútumot:
    # user.progress_saved_state = progress_json_string

    # Vagy ha a metódusod csak simán a dict-et várja és beállítja:
    user.set_progress_state(progress_json_string)  # Ezt ellenőrizni kell a User osztályban!

    user.last_progress_update = datetime.now(timezone.utc)
    db.session.commit()