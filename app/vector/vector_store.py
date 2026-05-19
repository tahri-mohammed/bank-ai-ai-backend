from app.database.postgres import get_connection


def to_pg_vector(embedding: list[float]) -> str:
    return "[" + ",".join(str(x) for x in embedding) + "]"


def save_chunk(document_title: str, content_type: str, chunk_text: str, embedding: list[float]):
    embedding_str = to_pg_vector(embedding)

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO document_chunks (
            document_title,
            content_type,
            chunk_text,
            embedding
        )
        VALUES (%s, %s, %s, %s::vector)
        """,
        (document_title, content_type, chunk_text, embedding_str)
    )

    connection.commit()
    cursor.close()
    connection.close()


def search_similar_chunks(query_embedding: list[float], limit: int = 3, product_filter: str | None = None):
    embedding_str = to_pg_vector(query_embedding)

    connection = get_connection()
    cursor = connection.cursor()

    if product_filter:
        cursor.execute(
            """
            SELECT
                id,
                document_title,
                content_type,
                chunk_text,
                1 - (embedding <=> %s::vector) AS score
            FROM document_chunks
            WHERE chunk_text ILIKE %s
            ORDER BY embedding <=> %s::vector
            LIMIT %s
            """,
            (embedding_str, f"%{product_filter}%", embedding_str, limit)
        )
    else:
        cursor.execute(
            """
            SELECT
                id,
                document_title,
                content_type,
                chunk_text,
                1 - (embedding <=> %s::vector) AS score
            FROM document_chunks
            ORDER BY embedding <=> %s::vector
            LIMIT %s
            """,
            (embedding_str, embedding_str, limit)
        )

    rows = cursor.fetchall()
    cursor.close()
    connection.close()

    return [
        {
            "id": row[0],
            "title": row[1],
            "type": row[2],
            "body": row[3],
            "score": round(float(row[4]), 3),
        }
        for row in rows
    ]
