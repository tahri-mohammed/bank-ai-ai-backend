def detect_language(text: str) -> str:
    text_lower = text.lower()

    french_words = ["je", "veux", "compte", "carte", "crédit", "ouvrir"]
    english_words = ["i", "want", "account", "card", "loan", "open"]
    arabic_chars = any("\u0600" <= char <= "\u06FF" for char in text)

    if arabic_chars:
        return "ar"

    if any(word in text_lower for word in french_words):
        return "fr"

    if any(word in text_lower for word in english_words):
        return "en"

    return "unknown"


def detect_intent(text: str) -> tuple[str, float]:
    text_lower = text.lower()

    if any(word in text_lower for word in ["ouvrir", "compte", "carte", "crédit", "épargne"]):
        return "PRODUCT_INFORMATION", 0.85

    if any(word in text_lower for word in ["problème", "bloqué", "application", "connexion", "mot de passe"]):
        return "DIGITAL_ASSISTANCE", 0.85

    if any(word in text_lower for word in ["comparer", "différence", "meilleur"]):
        return "COMPARISON", 0.80

    if any(word in text_lower for word in ["réclamation", "plainte", "erreur"]):
        return "COMPLAINT", 0.80

    if any(word in text_lower for word in ["conseillez", "recommande", "adapté"]):
        return "RECOMMENDATION", 0.80

    return "UNKNOWN", 0.50
