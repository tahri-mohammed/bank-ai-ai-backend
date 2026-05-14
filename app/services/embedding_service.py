from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")


def create_embedding(text: str) -> list[float]:
    embedding = model.encode(text)
    return embedding.tolist()
