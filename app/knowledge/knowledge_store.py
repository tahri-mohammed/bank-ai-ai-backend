import math
from app.vector.vector_store import save_chunk, search_similar_chunks
from app.services.chunking_service import chunk_text
from app.services.embedding_service import create_embedding
from app.services.query_normalizer import normalize_query
from app.vector.vector_store import save_chunk

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
        embedding = create_embedding(chunk)

        save_chunk(
            document_title=title,
            content_type=content_type,
            chunk_text=chunk,
            embedding=embedding,
        )

        chunk_objects.append({
            "chunk_id": index + 1,
            "text": chunk,
            "embedding": embedding,
        })

    item = {
        "id": len(knowledge_base) + 1,
        "title": title,
        "body": body,
        "type": content_type,
        "chunks": chunk_objects,
    }

    knowledge_base.append(item)

    return {
        "id": item["id"],
        "title": item["title"],
        "body": item["body"],
        "type": item["type"],
        "chunks_count": len(chunk_objects),
    }


def search_content(query: str):
    normalized_query = normalize_query(query)
    query_embedding = create_embedding(normalized_query)

    results = search_similar_chunks(query_embedding, limit=3)

    return [result for result in results if result["score"] > 0.30]


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
                "type": item["type"],
            })

    return recommendations[:1]
