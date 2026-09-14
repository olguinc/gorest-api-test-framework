import logging

logger = logging.getLogger("gorest_client")
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(levelname)s %(name)s: %(message)s"))
    logger.addHandler(handler)


def redact_headers(headers: dict) -> dict:
    redacted = dict(headers)
    if "Authorization" in redacted:
        redacted["Authorization"] = "Bearer ***"
    return redacted


def log_request(method: str, url: str, headers: dict, **kwargs) -> None:
    extra = {k: v for k, v in kwargs.items() if k in ("params", "json")}
    logger.info("--> %s %s headers=%s %s", method, url, redact_headers(headers), extra)


def log_response(method: str, url: str, status_code: int, elapsed_seconds: float) -> None:
    logger.info("<-- %s %s %s (%.3fs)", method, url, status_code, elapsed_seconds)
