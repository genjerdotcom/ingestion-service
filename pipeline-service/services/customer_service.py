from repositories.customer_repository import CustomerRepository
from utils.exceptions import AppException
from utils.logger import logger


class CustomerService:

    def __init__(self, db):
        self.repo = CustomerRepository(db)

    def get_customers(self, page: int, limit: int):
        logger.debug(f"[GET CUSTOMERS] page={page}, limit={limit}")

        try:
            
            offset = (page - 1) * limit
            result = self.repo.get_paginate(offset=offset, limit=limit)

            logger.debug(f"[GET CUSTOMERS SUCCESS] returned={result['total']}")

            return {
                "data": result["data"],
                "total": result["total"],
                "page": page,
                "limit": limit
            }
        except Exception as e:
            logger.error(f"[GET CUSTOMERS ERROR] {str(e)}")
            raise AppException("Failed to fetch customers", 500)

    def get_customer_by_id(self, customer_id: str):
        logger.debug(f"[GET CUSTOMER] id={customer_id}")

        try:
            data = self.repo.get_by_id(customer_id)

            if not data:
                logger.warning(f"[CUSTOMER NOT FOUND] id={customer_id}")
                raise AppException("Customer not found", 404)

            logger.debug(f"[GET CUSTOMER SUCCESS] id={customer_id}")

            return data

        except AppException:
            raise
        except Exception as e:
            logger.error(f"[GET CUSTOMER ERROR] id={customer_id} error={str(e)}")
            raise AppException("Failed to fetch customer", 500)