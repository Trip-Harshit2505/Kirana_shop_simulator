from fastapi import FastAPI
from app.routes import warehouse, shipping

app = FastAPI(title="Jumbotail Shipping Estimator")

app.include_router(warehouse.router)
app.include_router(shipping.router)

@app.get("/")
def health_check():
    return {"message": "Hello World!!!"}