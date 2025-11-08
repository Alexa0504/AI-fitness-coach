import json
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

try:
    client = genai.Client()
    GEMINI_MODEL = 'gemini-2.5-flash'
except Exception as e:
    print(f"FIGYELEM: Gemini Client inicializálása sikertelen: {e}. Mock adatokat szolgálunk ki API hiba esetén.")
    client = None


def get_mock_user_data(current_user_id: int) -> dict:
    """
    Ideiglenes függvény részletes felhasználói adatok generálására az AI promptjához.
    """
    return {
        "user_id": current_user_id,
        "age": 32,
        "weight_kg": 85,
        "height_cm": 185,
        "gender": "male",
        "goal": "muscle gain",
        "fitness_level": "intermediate",
        "weekly_workouts": 4,
        "dietary_restrictions": "none",
    }


def generate_plan(user_data: dict, plan_type: str) -> dict:
    """
    Meghívja a Gemini API-t egy személyre szabott terv generálására.

    :param user_data: A felhasználó adatai (angol kulcsokkal).
    :param plan_type: A generálandó terv típusa ('workout' vagy 'diet').
    :return: Szótár {"error": str | None, "plan_content_string": str | None}
    """

    if not client:
        error_msg = "Gemini API kliens nem elérhető."
        print(f"Hiba: {error_msg}")
        return {"error": error_msg, "plan_content_string": None}

    is_workout = (plan_type.lower() == "workout")

    prompt_data = {
        "age": user_data.get("age", 30),
        "weight_kg": user_data.get("weight_kg", 80),
        "height_cm": user_data.get("height_cm", 180),
        "goal": user_data.get("goal", "muscle gain"),
        "level": user_data.get("fitness_level", "intermediate"),
        "weekly_workouts": user_data.get("weekly_workouts", 4),
    }

    if is_workout:
        system_instruction = (
            "You are a professional fitness coach. Generate a 4-week workout plan. "
            "Your output must STRICTLY follow the JSON structure defined below."
        )
        plan_structure_description = {
            "type": "object",
            "properties": {
                "plan_name": {"type": "string", "description": "Descriptive name for the plan."},
                "plan_type": {"type": "string", "description": "Should be 'workout'."},
                "duration_days": {"type": "integer", "description": "Total duration in days (e.g., 28)."},
                "exercises": {
                    "type": "array",
                    "description": "List of daily exercises or rest days.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "day": {"type": "integer"},
                            "activity": {"type": "string",
                                         "description": "Exercise name (e.g., Bench Press) or 'Rest'."},
                            "sets": {"type": ["integer", "null"], "description": "Number of sets, or null if Rest."},
                            "reps": {"type": ["integer", "null"], "description": "Number of reps, or null if Rest."},
                            "duration_min": {"type": ["integer", "null"],
                                             "description": "Duration in minutes, or null if Set/Reps are used."},
                        },
                        "required": ["day", "activity"]
                    }
                },
                "note": {"type": "string", "description": "A final motivational or technical note."},
            },
            "required": ["plan_name", "plan_type", "duration_days", "exercises"]
        }

    else:  # diet plan
        system_instruction = (
            "You are a professional dietitian. Generate a 7-day example meal plan "
            "optimized for the user's goals. Your response must STRICTLY follow the JSON structure."
        )
        plan_structure_description = {
            "type": "object",
            "properties": {
                "plan_name": {"type": "string"},
                "plan_type": {"type": "string", "description": "Should be 'diet'."},
                "duration_days": {"type": "integer"},
                "calories_target": {"type": "integer", "description": "Target daily calorie intake."},
                "meals": {
                    "type": "array",
                    "description": "List of daily meal schedules.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "day": {"type": "integer"},
                            "breakfast": {"type": "string"},
                            "lunch": {"type": "string"},
                            "dinner": {"type": "string"},
                            "snack_1": {"type": ["string", "null"], "description": "Optional snack."},
                        },
                        "required": ["day", "breakfast", "lunch", "dinner"]
                    }
                },
                "macros_g": {
                    "type": "object",
                    "properties": {
                        "protein": {"type": "integer"},
                        "carbs": {"type": "integer"},
                        "fat": {"type": "integer"},
                    },
                    "required": ["protein", "carbs", "fat"]
                },
                "note": {"type": "string"},
            },
            "required": ["plan_name", "plan_type", "duration_days", "calories_target", "meals"]
        }

    user_prompt = f"""
    User Data: {json.dumps(prompt_data, indent=2)}

    Generate the {plan_type} plan following the rules. DO NOT include any extra text or explanation outside the JSON object.
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