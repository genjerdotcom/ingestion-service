import os
from utils.logger import logger
from utils.exceptions import AppException
from utils.transaction import transactional
from repositories.customer_repository import CustomerRepository
from dto.customer_dto import CustomerDTO
from utils.api_caller import fetch_customers_paginated

FLASK_HOST = os.getenv("FLASK_HOST", "localhost")
FLASK_PORT = os.getenv("FLASK_PORT", "5000")


class IngestionService:

    def __init__(self, db):
        self.db = db
        self.repo = CustomerRepository(db)

    @transactional
    def ingest(self):
        try:
            total_processed = 0

            logger.info("[INGEST START]")

            for data in fetch_customers_paginated():

                for item in data:
                    try:
                        dto = CustomerDTO(**item)
                        self.repo.upsert("customer_id", dto.dict())
                        total_processed += 1

                    except Exception as e:
                        logger.warning(f"[INVALID DATA] {str(e)}")

            logger.info(f"[INGEST DONE] total={total_processed}")

            return total_processed

        except AppException:
            raise
        except Exception as e:
            logger.error(f"[INGEST ERROR] {str(e)}")
            raise AppException("Ingestion failed", 500)