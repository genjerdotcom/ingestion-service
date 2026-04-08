from utils.logger import logger
from utils.exceptions import AppException
from sqlalchemy import func

class BaseRepository:

    def __init__(self, db, model):
        self.db = db
        self.model = model

    def create(self, data: dict):
        try:
            logger.debug(f"[CREATE REPOSITORY] {self.model.__name__}")
            obj = self.model(**data)
            self.db.add(obj)
            return obj
        except Exception as e:
            logger.error(f"[CREATE REPOSITORY ERROR] {str(e)}")
            raise AppException("Failed to create data", 500)

    def get_by_id(self, id):
        try:
            logger.debug(f"[GET REPOSITORY] {self.model.__name__}: {id}")
            return self.db.query(self.model).get(id)
        except Exception as e:
            logger.error(f"[GET REPOSITORY ERROR] {str(e)}")
            raise AppException("Failed to fetch data", 500)

    def get_paginate(self, offset=0, limit=10):
        try:
            logger.debug(f"[GET REPOSITORY ALL] {self.model.__name__}")

            query = self.db.query(
                self.model,
                func.count().over().label("total_count")
            ).offset(offset).limit(limit)

            results = query.all()

            if not results:
                return {
                    "data": [],
                    "total": 0
                }

            data = [row[0] for row in results]
            total = results[0][1]

            return {
                "data": data,
                "total": total
            }

        except Exception as e:
            logger.error(f"[GET REPOSITORY ALL ERROR] {str(e)}")
            raise AppException("Failed to fetch data", 500)

    def update(self, id, data: dict):
        try:
            logger.debug(f"[UPDATE REPOSITORY] {self.model.__name__}: {id}")

            obj = self.get_by_id(id)

            if not obj:
                raise AppException("Data not found", 404)

            for key, value in data.items():
                setattr(obj, key, value)

            return obj

        except AppException:
            raise
        except Exception as e:
            logger.error(f"[UPDATE REPOSITORY ERROR] {str(e)}")
            raise AppException("Failed to update data", 500)

    def delete(self, id):
        try:
            logger.debug(f"[DELETE REPOSITORY] {self.model.__name__}: {id}")

            obj = self.get_by_id(id)

            if not obj:
                raise AppException("Data not found", 404)

            self.db.delete(obj)
            return obj

        except AppException:
            raise
        except Exception as e:
            logger.error(f"[DELETE REPOSITORY ERROR] {str(e)}")
            raise AppException("Failed to delete data", 500)

    def upsert(self, pk_field: str, data: dict):
        try:
            logger.debug(f"[UPSERT REPOSITORY] {self.model.__name__}")

            pk_value = data.get(pk_field)

            obj = self.db.query(self.model).filter(
                getattr(self.model, pk_field) == pk_value
            ).first()

            if obj:
                for key, value in data.items():
                    setattr(obj, key, value)
                return obj

            return self.create(data)

        except Exception as e:
            logger.error(f"[UPSERT REPOSITORY ERROR] {str(e)}")
            raise AppException("Failed to upsert data", 500)