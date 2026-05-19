from app.knowledge.knowledge_store import search_content
from app.graph.graph_service import get_recommendations
from app.providers.provider_factory import get_provider
from app.graphrag.intent_entity_extractor import extract_intent_entities

def detect_product_from_sources(question: str, sources):
    question_upper = question.upper()

    if "PACK BLADI" in question_upper or "BLADI" in question_upper:
        return "PACK BLADI"

    if (
        "TELEPHONE" in question_upper
        or "TÉLÉPHONE" in question_upper
        or "APPLICATION" in question_upper
        or "MOBILE" in question_upper
        or "DISTANCE" in question_upper
        or "MN TELEPHONE" in question_upper
        or "MN TILIFON" in question_upper
    ):
        return "POCKET BANK"

    if "CHAABI NET" in question_upper:
        return "CHAABI NET"

    if "POCKET BANK" in question_upper:
        return "POCKET BANK"

    if "CARTE" in question_upper:
        return "CARTE « BLADI »"

    if "COMPTE EN DIRHAMS" in question_upper:
        return "COMPTE EN DIRHAMS"

    for source in sources:
        title = source.get("title", "")
        body = source.get("body", "")
        text = f"{title} {body}".upper()

        if "PACK BLADI" in text:
            return "PACK BLADI"

        if "POCKET BANK" in text:
            return "POCKET BANK"

        if "CHAABI NET" in text:
            return "CHAABI NET"

        if "COMPTE EN DIRHAMS" in text:
            return "COMPTE EN DIRHAMS"
            
        if "COMPTE" in question_upper or "N7EL COMPTE" in question_upper:
            return "COMPTE EN DIRHAMS"

        if "PACK BLADI" in question_upper:
            return "PACK BLADI"    

    return None


def answer_with_graphrag(question: str):
    initial_sources = search_content(question)

    if not initial_sources:
        return {
            "answer": "Je ne trouve pas cette information dans la base de connaissance validée.",
            "extraction": None,
            "detected_product": None,
            "recommendations": [],
            "sources": [],
        }

    extraction = extract_intent_entities(question, initial_sources)

    detected_product = extraction.get("product")
    needs_recommendation = extraction.get("needs_recommendation", False)

    vector_sources = search_content(
        question,
        product_filter=detected_product,
    )

    if not vector_sources:
        vector_sources = initial_sources

    graph_recommendations = []
    if detected_product and needs_recommendation:
        graph_recommendations = get_recommendations(detected_product)

    document_context = "\n\n".join(
        [
            f"Source: {item['title']}\nContenu: {item['body']}"
            for item in vector_sources
        ]
    )

    graph_context = "\n".join(
        [
            f"- {item['name']} : {item['reason']}"
            for item in graph_recommendations
        ]
    )

    prompt = f"""
Tu es un assistant bancaire marocain.

Règles :
1. Réponds uniquement à partir des sources validées.
2. N'invente aucune information.
3. Si la question est en darija, réponds en darija marocaine écrite en alphabet latin.
4. Si des recommandations graphe existent, propose-les seulement si elles sont utiles.
5. Réponse courte, claire et professionnelle.

Question :
{question}

Intention détectée :
{extraction}

Sources documentaires validées :
{document_context}

Recommandations issues du graphe métier :
{graph_context if graph_context else "Aucune recommandation graphe disponible."}

Réponds au format :
Réponse: ...
Recommandations: ...
"""

    provider = get_provider()
    generated = provider.generate(prompt)

    return {
        "answer": generated,
        "extraction": extraction,
        "detected_product": detected_product,
        "recommendations": graph_recommendations,
        "sources": vector_sources,
    }
    
    
def should_use_recommendations(question: str) -> bool:
    question_upper = question.upper()

    no_recommendation_keywords = [
        "QUELLE CARTE",
        "QUEL PRODUIT",
        "QUELS SONT",
        "C'EST QUOI",
        "CHNO",
        "ACHNO",
        "COMMENT",
        "KIFACH",
    ]

    recommendation_keywords = [
        "CONSEILLE",
        "RECOMMANDE",
        "PROPOSE",
        "ADAPTÉ",
        "ADAPTE",
        "BESOIN",
        "BAGHI",
        "BGHIT",
    ]

    if any(keyword in question_upper for keyword in recommendation_keywords):
        return True

    if any(keyword in question_upper for keyword in no_recommendation_keywords):
        return False

    return False
    
    
def enrich_query(question: str) -> str:
    q = question.lower()

    if "n7el compte" in q or "ouvrir compte" in q or "ouvrir un compte" in q:
        return "compte en dirhams ouverture compte CIN carte séjour contrat travail MDM"

    if "telephone" in q or "téléphone" in q or "mobile" in q or "application" in q:
        return "Chaabi Net Pocket Bank consulter compte smartphone banque à distance"

    if "pack bladi" in q or "carte liée" in q:
        return "Pack Bladi carte prépayée Bladi recharge gratuite"

    return question
