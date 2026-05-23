from fastapi import FastAPI

app = FastAPI(
    title="Data Standardization Agent MVP",
    version="0.1.0"
)


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