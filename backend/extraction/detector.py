def detect_scam(message: str, extracted: dict) -> dict:
    score = 0
    reasons = []
    msg = message.lower()

    keywords = [
        "otp", "kyc", "verify", "urgent",
        "send money", "refund", "account blocked"
    ]

    # Keyword-based risk
    for k in keywords:
        if k in msg:
            score += 1
            reasons.append(f"Keyword detected: {k}")

    # Entity-based risk (THIS WAS MISSING)
    if extracted.get("upi_ids"):
        score += 3
        reasons.append("UPI ID shared")

    if extracted.get("phone_numbers"):
        score += 2
        reasons.append("Phone number shared")

    if extracted.get("bank_accounts"):
        score += 4
        reasons.append("Bank account shared")

    if extracted.get("phishing_links"):
        score += 5
        reasons.append("Phishing link detected")

    # Final classification
    if score >= 7:
        risk_level = "HIGH"
        is_scam = True
    elif score >= 4:
        risk_level = "MEDIUM"
        is_scam = True
    else:
        risk_level = "LOW"
        is_scam = False

    return {
        "risk_score": score,
        "risk_level": risk_level,
        "is_scam": is_scam,
        "reasons": reasons
    }
