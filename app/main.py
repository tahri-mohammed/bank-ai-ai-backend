from app.api.knowledge_api import router as knowledge_router
from fastapi import FastAPI
from app.api.analyze_api import router as analyze_router
from app.api.generate_api import router as generate_router

app = FastAPI(title="Bank AI Backend")

app.include_router(analyze_router)
app.include_router(generate_router)
app.include_router(knowledge_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}
