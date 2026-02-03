def calculate_risk_score(entities: dict) -> dict:
    """
    Calculate a simple risk score based on extracted scam entities.
    """

    score = 0

    if entities.get("upi_ids"):
        score += 30

    if entities.get("bank_accounts"):
        score += 30

    if entities.get("ifsc_codes"):
        score += 20

    if entities.get("phishing_links"):
        score += 20

    if entities.get("phone_numbers"):
        score += 10

    if score >= 60:
        level = "HIGH"
    elif score >= 30:
        level = "MEDIUM"
    else:
        level = "LOW"

    return {
        "risk_score": score,
        "risk_level": level
    }
