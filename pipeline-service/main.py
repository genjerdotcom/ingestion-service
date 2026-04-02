from fastapi import FastAPI, Depends
from database import engine, Base, test_connection, get_db
from services.ingestion_service import IngestionService
from services.customer_service import CustomerService
from utils.response import success_response, pagination_response

app = FastAPI() 

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "ok"}

@app.on_event("startup")
def startup():
    test_connection()

@app.post("/api/ingest")
def ingest(db=Depends(get_db)):
    service = IngestionService(db)
    total = service.ingest()

    return success_response({
        "records_processed": total
    })

@app.get("/api/customers")
def get_customers(page: int = 1, limit: int = 10, db=Depends(get_db)):
    service = CustomerService(db)
    data = service.get_customers(page, limit)

    return pagination_response(data)


@app.get("/api/customers/{customer_id}")
def get_customer(customer_id: str, db=Depends(get_db)):
    service = CustomerService(db)
    data = service.get_customer_by_id(customer_id)

    return success_response(data)