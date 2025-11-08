import os
from google import genai
import json

try:
    client = genai.Client()
    GEMINI_MODEL = 'gemini-2.5-flash'
except Exception as e:
    print(f"Hiba a Gemini kliens inicializálásakor: {e}")
    client = None