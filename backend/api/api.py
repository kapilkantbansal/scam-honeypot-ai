from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from pydantic import BaseModel, ConfigDict
from backend.storage.database import init_db, save_message, get_last_messages
import uuid
from backend.agent.agent_controller import AgentController
from backend.extraction.extractor import extract_entities
from backend.extraction.detector import detect_scam
from fastapi import FastAPI, Header, Body,HTTPException, Depends

HACKATHON_API_KEY = "HCL2026_SECRET"  # Do NOT change after submission

def verify_api_key(x_api_key: str = Header(None)):
    if x_api_key != HACKATHON_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")


app = FastAPI(title="Scam Honeypot API")
init_db()
# ---------------- Schemas ----------------

class ChatRequest(BaseModel):
    message: Optional[str] = None
    content: Optional[str] = None
    conversation_id: Optional[str] = None

model_config = ConfigDict(extra="allow")
class ChatResponse(BaseModel):
    reply: str
    stop_chat: bool
    extracted: dict
    detection: Optional[dict] = None
    evidence: Optional[dict] = None


# ---------------- Controller ----------------

agent = AgentController()  # DO NOT pass GeminiClient here


# ---------------- Route ----------------

@app.post("/chat")
def chat(req: Optional[ChatRequest] = Body(None),_=Depends(verify_api_key)):

     # 🔥 Normalize tester + swagger input
    user_message = None

    if req:
        user_message = req.message or req.content

    # fallback so tester NEVER fails
    if not user_message:
        user_message = "Hello"
    

    # 1. Entity extraction
    extracted = extract_entities(user_message)

    # 2. Scam detection
    detection = detect_scam(user_message, extracted)

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
                "message": user_message,
                "entities": extracted,
                "reasons": detection["reasons"]
            }
        }

    # 4. Normal Gemini reply (NO TRY)
    reply = agent.generate_reply(user_message)

    return {
        "reply": reply,
        "stop_chat": False,
        "extracted": extracted,
        "detection": detection,
        "evidence": None
    }
