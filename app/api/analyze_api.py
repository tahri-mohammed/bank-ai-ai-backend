from fastapi import APIRouter
from app.schemas.analyze_schema import AnalyzeRequest, AnalyzeResponse
from app.services.intent_service import detect_language, detect_intent

router = APIRouter(prefix="/api/ai", tags=["AI Analysis"])


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze_text(request: AnalyzeRequest):
    language = detect_language(request.text)
    intent, confidence = detect_intent(request.text)

    return AnalyzeResponse(
        language=language,
        intent=intent,
        confidence=confidence
    )
