import requests
from utils.logger import logger
from utils.exceptions import AppException

def get_json(url: str, timeout: int = 5):
    try:
        logger.debug(f"[HTTP GET] {url}")

        response = requests.get(url, timeout=timeout)
        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as e:
        logger.error(f"[HTTP ERROR] {str(e)}")
        raise AppException("External API request failed", 500)