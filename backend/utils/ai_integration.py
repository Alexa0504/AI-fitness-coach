import json
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

try:
    client = genai.Client()
    GEMINI_MODEL = "gemini-2.5-flash"
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

    is_workout = plan_type.lower() == "workout"

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
                "plan_name": {"type": "string"},
                "plan_type": {"type": "string"},
                "duration_days": {"type": "integer"},
                "exercises": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "day": {"type": "integer"},
                            "activity": {"type": "string"},
                            "sets": {"type": "integer", "nullable": True},
                            "reps": {"type": "integer", "nullable": True},
                            "duration_min": {"type": "integer", "nullable": True},
                        },
                        "required": ["day", "activity"],
                    },
                },
                "note": {"type": "string"},
            },
            "required": ["plan_name", "plan_type", "duration_days", "exercises"],
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
                "plan_type": {"type": "string"},
                "duration_days": {"type": "integer"},
                "calories_target": {"type": "integer"},
                "meals": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "day": {"type": "integer"},
                            "breakfast": {"type": "string"},
                            "lunch": {"type": "string"},
                            "dinner": {"type": "string"},
                            "snack_1": {"type": "string", "nullable": True},
                        },
                        "required": ["day", "breakfast", "lunch", "dinner"],
                    },
                },
                "macros_g": {
                    "type": "object",
                    "properties": {
                        "protein": {"type": "integer"},
                        "carbs": {"type": "integer"},
                        "fat": {"type": "integer"},
                    },
                    "required": ["protein", "carbs", "fat"],
                },
                "note": {"type": "string"},
            },
            "required": ["plan_name", "plan_type", "duration_days", "calories_target", "meals"],
        }

    user_prompt = f"""
    User Data: {json.dumps(prompt_data, indent=2)}

    Generate the {plan_type} plan following the rules. DO NOT include any extra text or explanation outside the JSON object.
    """

    try:
        schema = genai.types.Schema(
            type=plan_structure_description["type"],
            properties=plan_structure_description["properties"],
            required=plan_structure_description.get("required", []),
        )

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=user_prompt,
            config=genai.types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                response_schema=schema,
            ),
        )

        plan_content_string = response.text

        if not plan_content_string:
            raise ValueError("Empty response from Gemini.")

        return {"error": None, "plan_content_string": plan_content_string}

    except Exception as e:
        import traceback

        print("Gemini API error details:\n", traceback.format_exc())
        return {"error": f"Gemini API hiba: {e}", "plan_content_string": None}