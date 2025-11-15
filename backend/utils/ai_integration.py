import json
import time
import random
from backend.utils.mock_data import get_mock_plan

def get_mock_user_data(current_user_id: int) -> dict:
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
    try:
        from google import genai
        from dotenv import load_dotenv
        import os

        load_dotenv()
        GEMINI_MODEL = "gemini-2.5-flash"
        client = genai.Client()
    except Exception as e:
        client = None

    is_workout = plan_type.lower() == "workout"

    prompt_data = {
        "age": user_data.get("age", 30),
        "weight_kg": user_data.get("weight_kg", 80),
        "height_cm": user_data.get("height_cm", 180),
        "goal": user_data.get("goal", "muscle gain"),
        "level": user_data.get("fitness_level", "intermediate"),
        "weekly_workouts": user_data.get("weekly_workouts", 4),
        "dietary_restrictions": user_data.get("dietary_restrictions", "none"),
    }

    if is_workout:
        system_instruction = (
            "You are a certified personal trainer. Generate a realistic 7-day workout plan "
            "tailored to the user data below. Each day includes a title and a list of exercises. "
            "Each exercise has a name, sets, reps, duration (optional), and notes (optional). "
            "Output ONLY valid JSON following the schema. No extra text."
        )

        plan_structure_description = {
            "type": "object",
            "properties": {
                "plan_name": {"type": "string"},
                "plan_type": {"type": "string"},
                "duration_days": {"type": "integer"},
                "days": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "day": {"type": "integer"},
                            "title": {"type": "string"},
                            "exercises": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "name": {"type": "string"},
                                        "sets": {"type": "integer"},
                                        "reps": {"type": "integer"},
                                        "duration_min": {"type": "integer"},
                                        "notes": {"type": "string"},
                                    },
                                    "required": ["name"]
                                },
                            },
                            "completed": {"type": "boolean"},
                        },
                        "required": ["day", "exercises"],
                    },
                },
                "note": {"type": "string"},
            },
            "required": ["plan_name", "plan_type", "duration_days", "days"],
        }

    else:
        system_instruction = (
            "You are a professional dietitian. Generate a 7-day diet plan optimized for the user. "
            "Output ONLY a JSON object that matches the schema. No explanations."
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
                            "snack": {"type": "string"},
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
                },
                "note": {"type": "string"},
            },
        }

    user_prompt = f"""
User Data: {json.dumps(prompt_data, indent=2)}

Generate the {plan_type} plan following the schema. Return only a JSON object.
"""

    max_retries = 3
    for attempt in range(max_retries):
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

            try:
                obj = json.loads(plan_content_string)
                if plan_type.lower() == "workout":
                    obj["duration_days"] = 7
                plan_content_string = json.dumps(obj)
            except:
                pass

            return {"error": None, "plan_content_string": plan_content_string}

        except Exception as e:
            err_str = str(e)
            if "503" in err_str or "UNAVAILABLE" in err_str:
                wait = 2 ** attempt + random.uniform(0.5, 1.5)
                time.sleep(wait)
                continue
            else:
                break

    mock_plan = get_mock_plan(plan_type)
    return {
        "error": "Gemini API temporarily unavailable — mock plan returned.",
        "plan_content_string": json.dumps(mock_plan),
    }
