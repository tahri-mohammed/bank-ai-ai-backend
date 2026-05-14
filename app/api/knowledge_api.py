from fastapi import APIRouter
from app.knowledge.knowledge_store import add_content, search_content
from app.providers.provider_factory import get_provider
from app.schemas.knowledge_schema import KnowledgeContentRequest, KnowledgeAnswerRequest

router = APIRouter(prefix="/api/knowledge", tags=["Knowledge"])


@router.post("/contents")
def create_knowledge_content(request: KnowledgeContentRequest):
    return add_content(
        title=request.title,
        body=request.body,
        content_type=request.content_type
    )


@router.post("/answer")
def answer_from_knowledge(request: KnowledgeAnswerRequest):
    results = search_content(request.question)

    if not results:
        return {
            "answer": "Je ne trouve pas cette information dans la base de connaissance validée.",
            "sources": []
        }

    context = "\n\n".join(
        [f"Titre: {item['title']}\nContenu: {item['body']}" for item in results]
    )

    prompt = f"""
Tu es un assistant bancaire marocain.
Réponds uniquement à partir du contexte validé ci-dessous.
Si l'information n'existe pas dans le contexte, dis que tu ne peux pas répondre.

Contexte:
{context}

Question client:
{request.question}
"""

    provider = get_provider()
    answer = provider.generate(prompt)

    return {
        "answer": answer,
        "sources": results
    }
