import logging
from functools import wraps
from pathlib import Path

LOG_FILE = Path(__file__).resolve().parent.parent / "logs" / "app.log"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger("laya")
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def log_calls(suppress_exceptions=()):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.info(
                "Function: %s | Args: %r | Kwargs: %r", func.__qualname__, args, kwargs
            )
            try:
                result = func(*args, **kwargs)
                logger.info("Function: %s | Completed", func.__qualname__)
                return result
            except Exception as error:
                logger.exception("Function: %s", func.__qualname__)
                if isinstance(error, suppress_exceptions):
                    return None
                raise

        return wrapper

    return decorator
