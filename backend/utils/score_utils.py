def calculate_mock_score(plan_type: str) -> int:
    """
    Returns a mock score based on the plan type.
    This is a placeholder for AI-driven scoring logic.
    """
    if plan_type.lower() == "workout":
        return 80
    elif plan_type.lower() == "diet":
        return 90
    return 70
