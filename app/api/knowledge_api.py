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

Règles obligatoires :
1. Réponds uniquement à partir du contexte validé.
2. N'ajoute aucun chiffre, délai, condition, avantage, risque, protection ou détail absent du contexte.
3. Ne fais pas de liste.
4. Réponds en maximum 2 phrases.
5. Si une information n'est pas explicitement présente, dis : "Cette information n'est pas disponible dans la base validée."
6. Réponds dans la langue de la question du client.

Contexte validé :
{context}

Question client :
{request.question}
"""

    answer = results[0]["body"]

    return {
        "answer": answer,
        "sources": results
    }
