from .regex_patterns import (
    UPI_REGEX,
    ACCOUNT_REGEX,
    IFSC_REGEX,
    PHONE_REGEX,
    URL_REGEX
)

def extract_entities(text: str) -> dict:
    """
    Extract scam-related entities from text.
    """

    return {
        "upi_ids": list(set(UPI_REGEX.findall(text))),
        "bank_accounts": list(set(ACCOUNT_REGEX.findall(text))),
        "ifsc_codes": list(set(IFSC_REGEX.findall(text))),
        "phone_numbers": list(set(PHONE_REGEX.findall(text))),
        "phishing_links": list(set(URL_REGEX.findall(text)))
    }


if __name__ == "__main__":
    sample_text = """
    Madam aapka KYC pending hai
    UPI id ram@ybl par payment karein
    Account number 458796321478
    IFSC SBIN0001234
    Link: http://secure-kyc-update.in
    """

    print(extract_entities(sample_text))
