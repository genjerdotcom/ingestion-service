import os
from utils.logger import logger
from utils.http_client import get_json

FLASK_HOST = os.getenv("FLASK_HOST", "localhost")
FLASK_PORT = os.getenv("FLASK_PORT", "5000")


def fetch_customers_paginated(page: int = 1, limit: int = 10):
    base_url = f"http://{FLASK_HOST}:{FLASK_PORT}"

    logger.info("[FETCH CUSTOMERS START]")

    while True:
        url = f"{base_url}/api/customers?page={page}&limit={limit}"

        result = get_json(url)
        data = result.get("data", [])

        if not data:
            logger.debug("[NO MORE DATA]")
            break

        yield data

        page += 1

    logger.info("[FETCH CUSTOMERS DONE]")