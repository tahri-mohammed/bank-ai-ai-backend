def normalize_query(query: str) -> str:
    q = query.lower()

    replacements = {
        "kifach": "comment",
        "n9der": "je peux",
        "nsayyer": "gérer",
        "floussi": "mon argent",
        "banque": "banque",
        "bghit": "je veux",
        "n7el": "ouvrir",
        "compte": "compte",
        "wach": "est ce que",
        "chno": "quoi",
        "carte": "carte",
    }

    for darija, fr in replacements.items():
        q = q.replace(darija, fr)

    return q
