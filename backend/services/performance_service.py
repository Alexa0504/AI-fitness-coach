from backend.models import UserGoal

class PerformanceService:
    @staticmethod
    def calculate_weekly_performance(user_id: int) -> float:
        weekly_goals = UserGoal.query.filter_by(user_id=user_id).all()
        if not weekly_goals:
            return 0.0
        completed_goals = sum(1 for g in weekly_goals if g.is_completed)
        return round((completed_goals / len(weekly_goals)) * 100, 2)
