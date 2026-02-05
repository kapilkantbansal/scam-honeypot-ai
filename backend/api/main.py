from fastapi import FastAPI
from backend.api.schemas import InputMessage
from backend.api.controller import HoneypotController

app = FastAPI(title="Scam Honeypot AI")

# Create controller instance
controller = HoneypotController(
    persona="Old confused victim",
    goal="Waste scammer time and extract information"
)


@app.post("/chat")
def chat(data: InputMessage):

    reply = controller.process_message(data.content)

    return {
        "reply": reply,
        "conversation": controller.conversation,
        "extracted": controller.extracted,
        "is_scam": controller.is_scam
    }


@app.get("/finalize")
def finalize():
    return controller.finalize()
