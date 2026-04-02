import logging
import os
import json
from datetime import datetime

LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG").upper()

COLORS = {
    "DEBUG": "\033[36m",
    "INFO": "\033[32m",
    "WARNING": "\033[33m",
    "ERROR": "\033[31m",
    "CRITICAL": "\033[35m",
}
RESET = "\033[0m"


class JsonFormatter(logging.Formatter):
    def format(self, record):
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

        level_name = record.levelname
        color = COLORS.get(level_name, "")
        level_colored = f"{color}{level_name}{RESET}"

        if isinstance(record.msg, dict):
            message = record.msg
        else:
            message = {"message": record.getMessage()}

        json_message = json.dumps(message, ensure_ascii=False)

        return f"{timestamp} - {level_colored} {json_message}"


def setup_logger():
    level = getattr(logging, LOG_LEVEL, logging.DEBUG)

    formatter = JsonFormatter()
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.handlers = [handler]

    for name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
        logger = logging.getLogger(name)
        logger.handlers = [handler]
        logger.propagate = False

    logging.getLogger("sqlalchemy.engine").handlers = [handler]

    return logging.getLogger("app")


logger = setup_logger()