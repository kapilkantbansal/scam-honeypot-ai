# main.py

from fastapi import FastAPI
from backend.api.schemas import InputMessage

app = FastAPI(title="Practice API Test")


@app.post("/test")
def test_api(data: InputMessage):
    return {
        "received_type": data.type,
        "received_content": data.content,
        "message": "API is working correctly"
    }

