import email
import email.policy
import re
from email.utils import parseaddr

from bs4 import BeautifulSoup

from utils.logger import log_calls
from utils.tokenizer import tokenize


@log_calls()
def parse_eml(file_path: str) -> dict:
    with open(file_path, "rb") as f:
        msg = email.message_from_binary_file(f, policy=email.policy.default)

    email_data: dict = {
        "from": parseaddr(str(msg.get("From", "")))[1],
        "subject": str(msg.get("Subject", "")),
    }

    plain_body = None
    html_body = None

    for part in msg.walk():
        if part.get_content_disposition() == "attachment":
            continue
        content_type = part.get_content_type()
        if content_type == "text/plain" and plain_body is None:
            plain_body = part.get_content()
        elif content_type == "text/html" and html_body is None:
            html_body = part.get_content()

    body = plain_body if plain_body and plain_body.strip() else html_body or ""

    soup = BeautifulSoup(body, "html.parser")
    for tag in soup(["script", "style", "head"]):
        tag.decompose()
    clean_body = soup.get_text(" ", strip=True)

    url_pattern = r'https?://[^\s<>"\')\]]+'
    urls = sorted(set(re.findall(url_pattern, clean_body)))

    clean_body = re.sub(url_pattern, "", clean_body)
    clean_body = re.sub(r"\s+", " ", clean_body).strip()

    email_data["body"] = tokenize(clean_body)
    email_data["urls"] = urls

    return email_data
