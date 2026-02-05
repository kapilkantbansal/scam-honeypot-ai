# backend/api/gemini_client.py
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

MODEL_NAME = "gemini-2.5-flash-lite"

class GeminiClient:
    def __init__(self):
        self.client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY")
        )

def generate_reply(persona: str, goal: str, scammer_message: str) -> str:
    client = GeminiClient()

    prompt = f"""
    Persona: {persona}
    Goal: {goal}

    Scammer said:
    {scammer_message}

    Respond like the persona while trying to waste scammer time.
    """

    return client.generate(prompt)
