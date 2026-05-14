import re


def split_into_sentences(text: str) -> list[str]:
    text = " ".join(text.split())

    sentences = re.split(r"(?<=[.!?؟])\s+", text)

    return [sentence.strip() for sentence in sentences if sentence.strip()]


def chunk_text(text: str, max_chars: int = 900) -> list[str]:
    sentences = split_into_sentences(text)

    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= max_chars:
            current_chunk += " " + sentence
        else:
            if current_chunk.strip():
                chunks.append(current_chunk.strip())

            current_chunk = sentence

    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks
