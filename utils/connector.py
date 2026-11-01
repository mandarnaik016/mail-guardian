import ollama

from utils.logger import log_calls

QUESTIONS = {
    "spam": {
        "type": "noul",
        "instructions": (
            "Determine whether the email is unsolicited bulk, junk or "
            "unwanted promotional communication. Consider its purpose, "
            "recipient consent and relevance."
        ),
        "criteria": {
            "true": (
                "Unsolicited advertisements, bulk marketing, junk mail, "
                "unwanted promotions or irrelevant mass communication."
            ),
            "false": (
                "Expected personal or business communication, requested "
                "updates, legitimate transactional emails or relevant "
                "notifications."
            ),
        },
    },
    "phishing": {
        "type": "noul",
        "instructions": (
            "Determine whether the email uses deception or impersonation "
            "to manipulate the recipient into disclosing sensitive information, "
            "performing fraudulent actions or interacting with malicious content."
        ),
        "criteria": {
            "true": (
                "Credential theft, financial fraud, impersonation, deceptive "
                "requests, malicious links or attachments, or social engineering."
            ),
            "false": (
                "Genuine communication without evidence of deception, "
                "fraudulent intent or malicious activity."
            ),
        },
    },
}


@log_calls()
def connect(email: dict) -> dict:
    client = ollama.Client(host="http://localhost:11434", timeout=60)
    response = client.systemone(model="laya", state=email, questions=QUESTIONS)
    spam = response.answers["spam"].noul
    phishing = response.answers["phishing"].noul
    return {
        "subject": email.get("subject"),
        "spam": f"{spam:.2%}",
        "phishing": f"{phishing:.2%}",
    }
