from .regex_patterns import (
    UPI_REGEX,
    ACCOUNT_REGEX,
    MASKED_ACCOUNT_REGEX,
    IFSC_REGEX,
    PHONE_REGEX,
    URL_REGEX,
    DOMAIN_REGEX
)


def _normalize_text(text: str) -> str:
    # collapse spaces around @ (ram @ ybl → ram@ybl)
    text = text.replace(" @ ", "@").replace("@ ", "@").replace(" @", "@")
    return text


def extract_entities(text: str) -> dict:
    # normalize noisy text first
    text = _normalize_text(text)

    # collect links (with and without http)
    links = set(URL_REGEX.findall(text)) | set(DOMAIN_REGEX.findall(text))

    return {
        "upi_ids": list(set(UPI_REGEX.findall(text))),
        "bank_accounts": list(set(
            ACCOUNT_REGEX.findall(text) +
            MASKED_ACCOUNT_REGEX.findall(text)
        )),
        "ifsc_codes": [c.upper() for c in set(IFSC_REGEX.findall(text))],
        "phone_numbers": list(set(PHONE_REGEX.findall(text))),
        "phishing_links": list(links)
    }


if __name__ == "__main__":
    sample_text = """
    Madam aapka KYC pending hai
    UPI id ram @ ybl par payment karein
    Account XXXX96321478
    IFSC sbin0001234
    Link: secure-kyc-update.in/login
    """

    print(extract_entities(sample_text))



