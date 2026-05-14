import math

from app.services.chunking_service import chunk_text
from app.services.embedding_service import create_embedding
from app.services.query_normalizer import normalize_query

knowledge_base = []


def cosine_similarity(vec1, vec2):
    dot = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = math.sqrt(sum(a * a for a in vec1))
    norm2 = math.sqrt(sum(b * b for b in vec2))

    if norm1 == 0 or norm2 == 0:
        return 0

    return dot / (norm1 * norm2)


def add_content(title: str, body: str, content_type: str):
    chunks = chunk_text(body)

    chunk_objects = []

    for index, chunk in enumerate(chunks):
        chunk_objects.append({
            "chunk_id": index + 1,
            "text": chunk,
            "embedding": create_embedding(chunk)
        })

    item = {
        "id": len(knowledge_base) + 1,
        "title": title,
        "body": body,
        "type": content_type,
        "chunks": chunk_objects
    }

    knowledge_base.append(item)

    return {
        "id": item["id"],
        "title": item["title"],
        "body": item["body"],
        "type": item["type"],
        "chunks_count": len(chunk_objects)
    }


def search_content(query: str):
    normalized_query = normalize_query(query)
    query_embedding = create_embedding(normalized_query)

    scored_results = []

    for item in knowledge_base:
        best_score = 0
        best_chunk = None

        for chunk in item["chunks"]:
            score = cosine_similarity(query_embedding, chunk["embedding"])

            if score > best_score:
                best_score = score
                best_chunk = chunk["text"]

        if best_score > 0.30:
            scored_results.append({
                "id": item["id"],
                "title": item["title"],
                "body": best_chunk,
                "type": item["type"],
                "score": round(best_score, 3)
            })

    scored_results.sort(key=lambda item: item["score"], reverse=True)

    return scored_results[:3]


def find_related_recommendations(main_results):
    recommendations = []

    main_text = " ".join(
        [f"{item['title']} {item['body']}" for item in main_results]
    ).lower()

    for item in knowledge_base:
        item_text = f"{item['title']} {item['body']}".lower()

        if any(result["id"] == item["id"] for result in main_results):
            continue

        if "compte" in main_text and "carte" in item_text:
            recommendations.append({
                "id": item["id"],
                "title": item["title"],
                "body": item["body"],
                "type": item["type"]
            })

    return recommendations[:1]
