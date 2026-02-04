def calculate_risk(extracted: dict, message: str) -> dict:
    score = 0
    reasons = []

    msg = message.lower()

    if extracted.get("upi_ids"):
        score += 3
        reasons.append("UPI ID detected")

    if extracted.get("phone_numbers"):
        score += 2
        reasons.append("Phone number detected")

    if extracted.get("bank_accounts"):
        score += 4
        reasons.append("Bank account detected")

    keywords = ["send money", "otp", "kyc", "verify", "urgent"]
    for k in keywords:
        if k in msg:
            score += 1
            reasons.append(f"Keyword: {k}")

    level = "LOW"
    if score >= 6:
        level = "HIGH"
    elif score >= 3:
        level = "MEDIUM"

    return {
        "risk_score": score,
        "risk_level": level,
        "is_scam": score >= 3,
        "reasons": list(set(reasons))
    }
