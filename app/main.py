from fastapi import FastAPI
from app.api.analyze_api import router as analyze_router

app = FastAPI(title="Bank AI Backend")


app.include_router(analyze_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
