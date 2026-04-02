from pydantic import BaseModel, EmailStr
from datetime import date, datetime

class CustomerDTO(BaseModel):
    customer_id: str
    first_name: str
    last_name: str
    email: EmailStr
    phone: str | None = None
    address: str | None = None
    date_of_birth: date
    account_balance: float
    created_at: datetime