from repositories.base import BaseRepository
from models.customer import Customer

class CustomerRepository(BaseRepository):

    def __init__(self, db):
        super().__init__(db, Customer)