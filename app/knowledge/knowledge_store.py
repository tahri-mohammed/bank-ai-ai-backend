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


def find_related_recommendations(main_results):
    recommendations = []

    main_text = " ".join(
        [f"{item['title']} {item['body']}" for item in main_results]
    ).lower()

    for item in knowledge_base:
        item_text = f"{item['title']} {item['body']}".lower()

        if item in main_results:
            continue

        if "compte" in main_text and "carte" in item_text:
            recommendations.append(item)

        if "carte" in main_text and "application" in item_text:
            recommendations.append(item)

        if "épargne" in main_text and "compte" in item_text:
            recommendations.append(item)

    return recommendations[:1]
