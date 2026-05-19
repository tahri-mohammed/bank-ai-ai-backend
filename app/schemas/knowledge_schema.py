from pydantic import BaseModel


class KnowledgeContentRequest(BaseModel):
    title: str
    body: str
    content_type: str


class KnowledgeAnswerRequest(BaseModel):
    question: str


class KnowledgeAnswerResponse(BaseModel):
    answer: str
    recommendation: str | None = None
    sources: list

