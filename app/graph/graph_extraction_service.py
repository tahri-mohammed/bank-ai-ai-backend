import unicodedata

from app.graph.graph_service import (
    create_product,
    create_relation,
    create_document,
    link_document_to_product,
)
from app.graph.product_catalog import PRODUCT_CATALOG


def normalize_text(text: str) -> str:
    text = text.upper()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(char for char in text if not unicodedata.combining(char))
    text = text.replace("’", "'").replace("‘", "'")
    text = text.replace("«", "").replace("»", "")
    text = text.replace("-", " ")
    text = " ".join(text.split())
    return text


def product_found(product_name: str, text: str) -> bool:
    return normalize_text(product_name) in normalize_text(text)


def extract_products_from_catalog(text: str) -> list[str]:
    detected = []

    for product in PRODUCT_CATALOG:
        if product_found(product, text):
            detected.append(product)

    return detected


def create_catalog_relations(products: list[str]):
    relations = []

    comptes = [p for p in products if p.startswith("COMPTE")]
    cartes = [
        p for p in products
        if p.startswith("CARTE") or p in ["ASFAR CARD", "I-C@RD", "SPEEDPAY"]
    ]
    packs = [p for p in products if p.startswith("PACK") or p.startswith("OCPACK")]
    digital = [
        p for p in products
        if p in ["CHAABI NET", "POCKET BANK", "CHAABI MOBILE", "CHAABI PHONE"]
    ]
    credits = [
        p for p in products
        if "CREDIT" in p or "PRET" in p or "SAKANE" in p or "BLADI IMMO" in p
    ]
    assistance = [
        p for p in products
        if "INJAD" in p or "ASSISTANCE" in p or "SCHENGEN" in p
    ]
    epargne = [
        p for p in products
        if p in [
            "AL IDDIKHAR CHAABI",
            "BON DE CAISSE",
            "COMPTE SUR CARNET",
            "DEPOT À TERME",
            "FONDS COMMUNS DE PLACEMENT",
            "PART SOCIALE",
        ]
    ]

    for compte in comptes:
        for service in digital:
            create_relation(
                compte,
                service,
                "HAS_SERVICE",
                "Ce service digital permet au client de consulter et gérer son compte à distance.",
            )
            relations.append(f"{compte} -[HAS_SERVICE]-> {service}")

        for carte in cartes[:6]:
            create_relation(
                compte,
                carte,
                "HAS_CARD",
                "Cette carte peut compléter le compte pour les retraits, paiements et achats.",
            )
            relations.append(f"{compte} -[HAS_CARD]-> {carte}")

    for pack in packs:
        for service in digital:
            create_relation(
                pack,
                service,
                "INCLUDES",
                "Ce service digital est inclus ou cohérent avec une offre packagée.",
            )
            relations.append(f"{pack} -[INCLUDES]-> {service}")

        for carte in cartes[:6]:
            create_relation(
                pack,
                carte,
                "INCLUDES",
                "Cette carte peut être associée à une offre packagée.",
            )
            relations.append(f"{pack} -[INCLUDES]-> {carte}")

    for compte in comptes:
        for produit in epargne[:3]:
            create_relation(
                compte,
                produit,
                "RECOMMENDS",
                "Ce produit d’épargne peut compléter la gestion bancaire du client.",
            )
            relations.append(f"{compte} -[RECOMMENDS]-> {produit}")

        for produit in credits[:3]:
            create_relation(
                compte,
                produit,
                "RECOMMENDS",
                "Ce financement peut répondre à un besoin complémentaire du client.",
            )
            relations.append(f"{compte} -[RECOMMENDS]-> {produit}")

    for pack in packs:
        for produit in assistance[:3]:
            create_relation(
                pack,
                produit,
                "RECOMMENDS",
                "Ce service d’assistance peut compléter l’offre packagée.",
            )
            relations.append(f"{pack} -[RECOMMENDS]-> {produit}")

    return relations


def extract_graph_from_text(text: str, document_title: str = "Unknown document", content_type: str = "DOCUMENT"):
    create_document(document_title, content_type)

    products = extract_products_from_catalog(text)

    for product in products:
        create_product(
            product,
            f"Produit ou service détecté depuis le catalogue officiel : {product}",
        )

        link_document_to_product(document_title, product)

    relations = create_catalog_relations(products)

    return {
        "document": document_title,
        "products_count": len(products),
        "products": products,
        "relations_count": len(relations),
        "relations": relations[:80],
    }
