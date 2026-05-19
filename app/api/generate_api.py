import os
from fastapi import APIRouter
from app.providers.provider_factory import get_provider
from app.schemas.generate_schema import GenerateRequest, GenerateResponse

router = APIRouter(prefix="/api/ai", tags=["AI Generation"])


@router.post("/generate", response_model=GenerateResponse)
def generate_response(request: GenerateRequest):
    provider = get_provider()
    response = provider.generate(request.prompt)

    return GenerateResponse(
        response=response,
        provider=os.getenv("LLM_PROVIDER", "ollama")
    )
