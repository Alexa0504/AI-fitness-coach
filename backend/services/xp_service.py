from datetime import datetime, timedelta
from models import db, User

WEEKLY_GOAL_XP = 300
LEVEL_XP_THRESHOLD = 1200

def award_weekly_goals_xp(user: User, weeks: int = 1):
    add_xp(user, WEEKLY_GOAL_XP * weeks, reason=f"weekly_goals_{weeks}_weeks")
    db.session.commit()

def add_xp(user: User, amount: int, reason: str = None):
    if amount == 0:
        return user.xp, user.level, False

    new_xp = user.xp + int(amount)
    carry_over = False

    while new_xp >= LEVEL_XP_THRESHOLD:
        new_xp -= LEVEL_XP_THRESHOLD
        user.level += 1
        carry_over = True

    user.xp = new_xp
    db.session.add(user)
    db.session.commit()
    return user.xp, user.level, carry_over

def xp_status(user: User):
    remaining = max(0, LEVEL_XP_THRESHOLD - user.xp)
    return {
        "xp": user.xp,
        "level": user.level,
        "xp_to_next_level": remaining,
        "level_xp_threshold": LEVEL_XP_THRESHOLD
    }
