knowledge_base = []


def add_content(title: str, body: str, content_type: str):
    item = {
        "id": len(knowledge_base) + 1,
        "title": title,
        "body": body,
        "type": content_type
    }
    knowledge_base.append(item)
    return item


def search_content(query: str):
    query_lower = query.lower()
    results = []

    for item in knowledge_base:
        text = f"{item['title']} {item['body']}".lower()

        if any(word in text for word in query_lower.split()):
            results.append(item)

    return results
