def detect_language(text: str) -> str:
    text_lower = text.lower()

    arabic_chars = any("\u0600" <= char <= "\u06FF" for char in text)

    darija_words = [
        "bghit", " بغيت", "n7el", "nhel", "compte", "flous",
        "kart", "carte", "kredit", "credit", "wach", "fin",
        "mabghach", "ma khdamch", "khassni", "3andi", "mouchkil",
        "solde", "virement", "application", "pocket bank"
    ]

    french_words = [
        "je", "veux", "compte", "carte", "crédit", "ouvrir",
        "problème", "application", "virement", "solde"
    ]

    english_words = [
        "i", "want", "account", "card", "loan", "open",
        "problem", "transfer", "balance"
    ]

    if any(word in text_lower for word in darija_words):
        return "darija"

    if arabic_chars:
        return "ar"

    if any(word in text_lower for word in french_words):
        return "fr"

    if any(word in text_lower for word in english_words):
        return "en"

    return "unknown"


def detect_intent(text: str) -> tuple[str, float]:
    text_lower = text.lower()

    product_words = [
        "ouvrir", "compte", "carte", "crédit", "credit", "kredit",
        "épargne", "epargne", "n7el", "nhel", "bghit compte",
        "بغيت نحل", "حساب", "بطاقة", "قرض"
    ]

    digital_words = [
        "problème", "probleme", "bloqué", "bloque", "connexion",
        "mot de passe", "application", "pocket bank", "chaabi net",
        "ma khdamch", "mabghach", "mouchkil", "مشكل", "تطبيق"
    ]

    comparison_words = [
        "comparer", "différence", "difference", "meilleur",
        "afضل", "شنو حسن", "wach hsen", "hsen", "compare"
    ]

    complaint_words = [
        "réclamation", "reclamation", "plainte", "erreur",
        "شكوى", "احتجاج", "ghalat", "erreur"
    ]

    recommendation_words = [
        "conseillez", "conseil", "recommande", "adapté", "adapte",
        "chno t9ter7", "شنو تنصحني", "شنو مناسب", "recommend"
    ]

    escalation_words = [
        "conseiller", "agence", "humain", "appel", "urgence",
        "بغيت نهضر مع شي واحد", "agent", "support"
    ]

    if any(word in text_lower for word in product_words):
        return "PRODUCT_INFORMATION", 0.85

    if any(word in text_lower for word in digital_words):
        return "DIGITAL_ASSISTANCE", 0.85

    if any(word in text_lower for word in comparison_words):
        return "COMPARISON", 0.80

    if any(word in text_lower for word in complaint_words):
        return "COMPLAINT", 0.80

    if any(word in text_lower for word in recommendation_words):
        return "RECOMMENDATION", 0.80

    if any(word in text_lower for word in escalation_words):
        return "ESCALATION", 0.80

    return "UNKNOWN", 0.50
