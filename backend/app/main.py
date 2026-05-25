from fastapi import FastAPI

from app.standardization.router import router as standardization_router

app = FastAPI(
    title="Data Standardization Agent MVP",
    version="0.1.0"
)

app.include_router(standardization_router)


@app.get("/")
def home():
    return {
        "message": "Data Standardization Agent MVP is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }