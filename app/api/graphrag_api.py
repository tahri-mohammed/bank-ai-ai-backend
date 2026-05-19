from fastapi import APIRouter
from pydantic import BaseModel

from app.graphrag.graphrag_service import answer_with_graphrag

router = APIRouter(prefix="/api/graphrag", tags=["GraphRAG"])


class GraphRAGRequest(BaseModel):
    question: str


@router.post("/answer")
def graphrag_answer(request: GraphRAGRequest):
    return answer_with_graphrag(request.question)
