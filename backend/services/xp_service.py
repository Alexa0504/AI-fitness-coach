from backend.models import db, User

XP_PER_WEEK = 300
XP_FOR_LEVEL_UP = 1200

def update_weekly_xp(user: User):
    weekly_goals = user.user_goals
    if not weekly_goals:
        return False, "No weekly goals set."

    completed_goals = sum(1 for g in weekly_goals if g.is_completed)
    total_goals = len(weekly_goals)

    if total_goals == 0:
        return False, "No goals for this week."

    xp_gained = round((completed_goals / total_goals) * XP_PER_WEEK)
    if xp_gained == 0:
        return False, "No weekly goals completed."

    user.xp += xp_gained
    leveled_up = check_level_up(user)
    db.session.commit()

    return True, f"XP updated: +{xp_gained}{' Level up!' if leveled_up else ''}"

def check_level_up(user: User):
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
