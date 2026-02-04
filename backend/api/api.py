from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

from backend.storage.database import init_db, save_message, get_last_messages
import uuid
from backend.agent.agent_controller import AgentController
from backend.extraction.extractor import extract_entities
from backend.extraction.detector import detect_scam

app = FastAPI(title="Scam Honeypot API")
init_db()
# ---------------- Schemas ----------------

class ChatRequest(BaseModel):
    message: str
conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    reply: str
    stop_chat: bool
    extracted: dict
    detection: Optional[dict] = None
    evidence: Optional[dict] = None


# ---------------- Controller ----------------

agent = AgentController()  # DO NOT pass GeminiClient here


# ---------------- Route ----------------

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):

    

    # 1. Entity extraction
    extracted = extract_entities(req.message)

    # 2. Scam detection
    detection = detect_scam(req.message, extracted)

    if not detection:
        detection = {
            "risk_score": 0,
            "risk_level": "LOW",
            "is_scam": False,
            "reasons": []
        }

    # 3. High-risk → block
    if detection["is_scam"] and detection["risk_score"] >= 5:
        return {
            "reply": "⚠️ This conversation has been flagged as a potential scam. Interaction blocked.",
            "stop_chat": True,
            "extracted": extracted,
            "detection": detection,
            "evidence": {
                "message": req.message,
                "entities": extracted,
                "reasons": detection["reasons"]
            }
        }

    # 4. Normal Gemini reply (NO TRY)
    reply = agent.generate_reply(req.message)

    return {
        "reply": reply,
        "stop_chat": False,
        "extracted": extracted,
        "detection": detection,
        "evidence": None
    }
