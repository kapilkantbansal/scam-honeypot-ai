from datetime import datetime

def build_evidence(message: str, extracted: dict, detection: dict) -> dict:
    return {
        "message": message,
        "extracted": extracted,
        "risk_score": detection["risk_score"],
        "risk_level": detection["risk_level"],
        "reasons": detection["reasons"],
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
