from backend.models import db

LEVEL_XP_THRESHOLD = 1200
WEEKLY_GOAL_XP = 300

def add_xp(user, amount):
    new_xp = user.xp + amount

    # Level up loop
    leveled_up = False
    while new_xp >= LEVEL_XP_THRESHOLD:
        new_xp -= LEVEL_XP_THRESHOLD
        user.level += 1
        leveled_up = True

    user.xp = new_xp
    db.session.commit()

    return {"xp": user.xp, "level": user.level, "leveled_up": leveled_up}


def xp_status(user):
    return {
        "xp": user.xp,
        "level": user.level,
        "xp_to_next": LEVEL_XP_THRESHOLD - user.xp,
    }
