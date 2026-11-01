import json
import time

from utils.connector import connect
from utils.logger import log_calls, logger
from utils.parser import parse_eml

MAX_PAYLOAD_SIZE = 1700


@log_calls()
def is_valid(data: dict) -> bool:
    return len(json.dumps(data, ensure_ascii=False)) <= MAX_PAYLOAD_SIZE


@log_calls()
def sanitize(data: dict) -> dict | None:
    payload = data.copy()

    if is_valid(payload):
        return payload

    payload.pop("urls", None)

    if is_valid(payload):
        return payload

    logger.warning(
        "Payload skipped | Reason: Exceeds %s characters | Subject: %s",
        MAX_PAYLOAD_SIZE,
        data.get("subject", "Unknown"),
    )

    return None


@log_calls()
def process_email(path):
    data = sanitize(parse_eml(path))
    if not data:
        return None
    start = time.perf_counter()
    response = connect(data)
    return response, time.perf_counter() - start


@log_calls()
def colorize(value):
    value = float(str(value).replace("%", ""))
    color = (
        "red"
        if value >= 75
        else "orange1"
        if value >= 50
        else "yellow"
        if value >= 25
        else "green"
    )
    return f"[{color}]{value:.1f}%[/{color}]"
