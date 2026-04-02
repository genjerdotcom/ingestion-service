from utils.logger import logger
from utils.exceptions import AppException

def transactional(func):
    def wrapper(self, *args, **kwargs):
        try:
            logger.debug(f"[TX START] {func.__name__}")

            result = func(self, *args, **kwargs)

            self.db.commit()
            logger.debug(f"[TX COMMIT] {func.__name__}")

            return result

        except AppException as ae:
            self.db.rollback()
            logger.warning(f"[TX ROLLBACK][APP ERROR] {ae.message}")
            raise ae

        except Exception as e:
            self.db.rollback()
            logger.error(f"[TX ROLLBACK][SYSTEM ERROR] {str(e)}")
            raise AppException("Database transaction failed", 500)

    return wrapper