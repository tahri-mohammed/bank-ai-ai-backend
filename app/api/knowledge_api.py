from fastapi import APIRouter, UploadFile, File
import os
import shutil
from fastapi import APIRouter, UploadFile, File
from app.services.pdf_service import extract_text_from_pdf
from app.knowledge.knowledge_store import (
    add_content,
    search_content,
    find_related_recommendations,
)
from app.providers.provider_factory import get_provider
from app.schemas.knowledge_schema import (
    KnowledgeContentRequest,
    KnowledgeAnswerRequest,
)

router = APIRouter(prefix="/api/knowledge", tags=["Knowledge"])


@router.post("/contents")
def create_knowledge_content(request: KnowledgeContentRequest):
    return add_content(
        title=request.title,
        body=request.body,
        content_type=request.content_type,
    )


@router.post("/answer")
def answer_from_knowledge(request: KnowledgeAnswerRequest):
    results = search_content(request.question)

    if not results:
        return {
            "answer": "Je ne trouve pas cette information dans la base de connaissance validée.",
            "recommendation": None,
            "sources": [],
        }

    recommendation_sources = find_related_recommendations(results)

    main_context = "\n\n".join(
        [f"Titre: {item['title']}\nContenu: {item['body']}" for item in results]
    )

    recommendation_context = "\n\n".join(
        [
            f"Titre: {item['title']}\nContenu: {item['body']}"
            for item in recommendation_sources
        ]
    )

    prompt = f"""
Tu es un assistant bancaire marocain.

Règles strictes :
1. Réponds uniquement à partir du contenu validé.
2. Si la question contient des mots darija en alphabet latin comme chno, bghit, wach, ndir, n7el, khassni, jawab obligatoirement en darija marocaine écrite en alphabet latin.
3. Tu ne dois ajouter aucun fait absent du contenu validé.
4. Tu peux recommander uniquement si une source de recommandation est fournie.
5. La recommandation doit être liée au besoin du client.
6. Si aucune recommandation validée n'est fournie, n'en propose pas.
7. Réponds court, clair et professionnel.

Question client :
{request.question}

Contenu validé pour répondre :
{main_context}

Contenu validé pour recommandation :
{recommendation_context if recommendation_context else "Aucune recommandation validée disponible."}

Retourne exactement ce format :
Réponse: ...
Recommandation: ...
"""

    provider = get_provider()
    generated = provider.generate(prompt)

    answer = generated
    recommendation = None

    if "Recommandation:" in generated:
        parts = generated.split("Recommandation:", 1)
        answer = parts[0].replace("Réponse:", "").strip()
        recommendation = parts[1].strip()

        if recommendation.lower() in ["", "aucune", "none", "aucune recommandation"]:
            recommendation = None
            
        if recommendation and "aucune recommandation" in recommendation.lower():
            recommendation = None    

    return {
        "answer": answer,
        "recommendation": recommendation,
        "sources": results + recommendation_sources,
    }
@router.post("/upload-pdf")
def upload_pdf(file: UploadFile = File(...)):
    os.makedirs("uploads", exist_ok=True)

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    extracted_text = extract_text_from_pdf(file_path)

    content = add_content(
        title=file.filename,
        body=extracted_text,
        content_type="DOCUMENT"
    )

    return {
        "message": "PDF ingéré avec succès",
        "content": content
    }
