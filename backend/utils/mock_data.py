def get_mock_plan(plan_type: str):
    """
    Returns a mock AI-generated plan for testing purposes.
    Later this will be replaced with a real Gemini API call.
    """

    if plan_type == "workout":
        return {
            "plan_name": "AI Full Body Workout",
            "duration_days": 7,
            "exercises": [
                {"day": 1, "activity": "Push-ups", "sets": 3, "reps": 15},
                {"day": 2, "activity": "Squats", "sets": 3, "reps": 20},
                {"day": 3, "activity": "Plank", "duration_sec": 60},
                {"day": 4, "activity": "Jogging", "duration_min": 30},
                {"day": 5, "activity": "Rest"},
                {"day": 6, "activity": "Burpees", "sets": 3, "reps": 10},
                {"day": 7, "activity": "Stretching", "duration_min": 15},
            ]
        }

    elif plan_type == "diet":
        return {
            "plan_name": "AI Healthy Meal Plan",
            "duration_days": 7,
            "meals": [
                {"day": 1, "breakfast": "Oatmeal + Banana", "lunch": "Chicken salad", "dinner": "Grilled salmon"},
                {"day": 2, "breakfast": "Smoothie", "lunch": "Rice + Veggies", "dinner": "Soup + Bread"},
                {"day": 3, "breakfast": "Eggs + Toast", "lunch": "Pasta + Spinach", "dinner": "Tuna salad"},
            ]
        }

    else:
        return {
            "plan_name": "Generic Fitness Plan",
            "duration_days": 7,
            "message": "Mock data for testing only."
        }
