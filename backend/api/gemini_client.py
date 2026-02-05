import os
from dotenv import load_dotenv
import google.generativeai as genai
from backend.agent.rules import AGENT_RULES
from google.generativeai.types import GenerationConfig

load_dotenv()

MODEL_NAME = "gemini-2.5-flash-lite"

class GeminiClient:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel(MODEL_NAME)

    def generate(self, prompt: str) -> str:
     response = self.client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

     text = response.text.strip()

    # HARD ENFORCEMENT
     sentences = text.split(".")
     sentences = sentences[:2]

     short_sentences = []
     for s in sentences:
        words = s.split()
        short_sentences.append(" ".join(words[:20]))
        return ". ".join(short_sentences).strip()


def generate_reply(persona: str, goal: str, scammer_message: str) -> str:
    client = GeminiClient()

    rules_text = "\n".join(AGENT_RULES)
    prompt = f"""
    Follow these rules STRICTLY:
{rules_text}
Persona: {persona}
Goal: {goal}

Scammer said:
{scammer_message}

"""

    return client.generate(prompt)
