from fastapi import FastAPI

app = FastAPI(title="Bank AI Backend")

@app.get("/health")
def health_check():
    return {"status": "ok"}
