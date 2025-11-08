import os
from google import genai
import json

try:
    client = genai.Client()
    GEMINI_MODEL = 'gemini-2.5-flash'
except Exception as e:
    print(f"Hiba a Gemini kliens inicializálásakor: {e}")
    client = None


def generate_plan(user_data: dict, plan_type: str) -> dict:
    """
    Gemini API hívása személyre szabott edzés- vagy táplálkozási terv generálására.

    :param user_data: A felhasználó adatai.
    :param plan_type: A generálandó terv típusa ('workout' vagy 'diet').
    :return: A generált tervet tartalmazó dict (JSON stringként).
    """

    if not client:
        return {"error": "Gemini API kliens nem elérhető.", "plan_content_string": None}

    is_workout = (plan_type.lower() == "workout")

    example_data = {
        "age": user_data.get("kor", 30),
        "weight": user_data.get("súly", 80),
        "height": user_data.get("magasság", 180),
        "goal": user_data.get("cél", "muscle gain"),
        "level": user_data.get("szint", "intermediate"),
        "weekly_workouts": user_data.get("heti_edzesnapok", 4),
    }

    if is_workout:
        system_instruction = (
            "You are a professional fitness coach. Your task is to generate a personalized "
            "4-day workout plan based on the user's data. "
            "Your output must STRICTLY follow the JSON structure defined below."
        )
        plan_structure_description = {
            "plan_name": "4 Day Muscle Building Plan",
            "plan_type": "workout",
            "duration_days": 28,
            "exercises": [
                {
                    "day": 1,
                    "activity": "Bench Press",
                    "sets": 3,
                    "reps": 8,
                    "rest_sec": 90
                },
                # ...
            ],
            "note": "Focus on progressive overload."
        }

    else:  # diet plan
        system_instruction = (
            "You are a professional dietitian. Your task is to generate a personalized 1-day meal plan "
            "optimized for the user's goals. Your response must STRICTLY follow the JSON structure defined below."
        )
        plan_structure_description = {
            "plan_name": "Optimal Diet Plan (1 Day)",
            "plan_type": "diet",
            "duration_days": 1,
            "calories_target": 2500,
            "meals": [
                {"day": 1, "breakfast": "Oatmeal with berries and protein powder",
                 "lunch": "Chicken salad with mixed greens", "dinner": "Salmon with roasted vegetables"},
            ],
            "macros_g": {"protein": 180, "carbs": 250, "fat": 80},
        }

    user_prompt = f"""
    User Data: {json.dumps(example_data)}

    Generate the {plan_type} plan. The output must STRICTLY be in the specified JSON format.
    DO NOT include any extra text or explanation outside the JSON object.
    """

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=user_prompt,
            config=genai.types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                response_schema=genai.types.Schema.from_dict(plan_structure_description)
            )
        )

        plan_content_string = response.text

        if not plan_content_string:
            raise ValueError("Empty response from Gemini.")

        return {"error": None, "plan_content_string": plan_content_string}

    except Exception as e:
        print(f"Hiba a Gemini API hívásban: {e}")
        return {"error": f"Gemini API hiba: {e}", "plan_content_string": None}