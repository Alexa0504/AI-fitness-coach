from backend.models import db, User

XP_PER_WEEK = 300
XP_FOR_LEVEL_UP = 1200


def update_weekly_xp(user: User):
    """Adds XP if weekly goals were completed."""
    completed_goals = [g for g in user.user_goals if g.is_completed]

    if len(completed_goals) == 0:
        return False, "No weekly goals completed."

    user.xp += XP_PER_WEEK
    check_level_up(user)

    db.session.commit()
    return True, "XP updated."


def check_level_up(user: User):
    """Increases level when XP reaches threshold."""
    leveled_up = False

    while user.xp >= XP_FOR_LEVEL_UP:
        user.level += 1
        user.xp -= XP_FOR_LEVEL_UP
        leveled_up = True

    return leveled_up


def get_xp_status(user: User):
    return {
        "xp": user.xp,
        "level": user.level,
        "xpToNext": XP_FOR_LEVEL_UP - user.xp
    }

