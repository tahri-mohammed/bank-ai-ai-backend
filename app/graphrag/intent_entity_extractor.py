import json
import re

from app.providers.provider_factory import get_provider


def safe_json_parse(text: str) -> dict:
    try:
        return json.loads(text)
    except Exception:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except Exception:
                pass

    return {
        "intent": "UNKNOWN",
        "product": None,
        "needs_recommendation": False,
        "language": "unknown",
    }


def extract_intent_entities(question: str, sources: list[dict]) -> dict:
    context = "\n\n".join(
        [
            f"Titre: {source.get('title')}\nContenu: {source.get('body')}"
            for source in sources[:3]
        ]
    )

    prompt = f"""
Tu es un extracteur d'intention pour un agent bancaire marocain.

À partir de la question client et des sources, retourne uniquement un JSON valide.

Intentions possibles :
- PRODUCT_INFORMATION
- OPEN_ACCOUNT
- DIGITAL_ASSISTANCE
- COMPARISON
- RECOMMENDATION
- COMPLAINT
- UNKNOWN

Produits possibles :
- COMPTE EN DIRHAMS
- COMPTE EN DEVISES
- COMPTE EN DIRHAMS CONVERTIBLES
- COMPTE COURANT
- PACK BLADI
- CARTE « BLADI »
- CARTE « LA POPULAIRE »
- CHAABI NET
- POCKET BANK
- COMPTE SUR CARNET
- BON DE CAISSE
- AL IDDIKHAR CHAABI
- INJAD ACHAMIL
- INJAD SALAMA

Règles :
1. Si le client demande conseil ou dit "bghit", "conseille", "recommande", "chno nzid", mets needs_recommendation à true.
2. Si le client demande seulement une définition, une condition, une carte liée ou une explication, mets needs_recommendation à false.
3. Si la question parle de téléphone, application, mobile ou gestion à distance, produit = POCKET BANK.
4. Si la question parle d'ouverture de compte, produit = COMPTE EN DIRHAMS.
5. Si la question parle du pack Bladi, produit = PACK BLADI.
6. Détecte la langue : fr, darija, ar, en.

Question :
{question}

Sources :
{context}

Format attendu uniquement :
{{
  "intent": "...",
  "product": "...",
  "needs_recommendation": true,
  "language": "..."
}}
"""

    provider = get_provider()
    result = provider.generate(prompt)

    data = safe_json_parse(result)

    return {
        "intent": data.get("intent", "UNKNOWN"),
        "product": data.get("product"),
        "needs_recommendation": bool(data.get("needs_recommendation", False)),
        "language": data.get("language", "unknown"),
    }
