import sys
import os

# Allow imports from project root
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from fastapi import FastAPI
from pydantic import BaseModel
from backend.api.controller import HoneypotController

app = FastAPI(title="Scam Honeypot API")

# 🔒 Single controller instance (demo / session-like behavior)
controller = HoneypotController(
    persona="""
You are a 65-year-old Indian retired man.
You speak politely in Hinglish.
You are slow and confused with technology.
You never refuse directly.
You ask people to repeat details slowly.
Avoid repeating the same phrase every time.
""",
    goal="Extract payment details like UPI ID without alerting the scammer."
)

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str
    stop_chat: bool
    extracted: dict

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    reply = controller.process_message(req.message)

    extracted_data = (
        controller.extracted.dict()
        if hasattr(controller.extracted, "dict")
        else controller.extracted.model_dump()
    )

    return {
        "reply": reply,
        "stop_chat": controller.stop_chat,
        "extracted": extracted_data
    }
