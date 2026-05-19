from app.graph.neo4j_connection import get_driver


def create_product(name: str, description: str):
    driver = get_driver()

    with driver.session() as session:
        session.run(
            """
            MERGE (p:Product {name: $name})
            SET p.description = $description
            """,
            name=name,
            description=description
        )

    return {"name": name, "description": description}


def create_recommendation(source_product: str, target_product: str, reason: str):
    driver = get_driver()

    with driver.session() as session:
        session.run(
            """
            MERGE (source:Product {name: $source_product})
            MERGE (target:Product {name: $target_product})
            MERGE (source)-[r:RECOMMENDS]->(target)
            SET r.reason = $reason
            """,
            source_product=source_product,
            target_product=target_product,
            reason=reason
        )

    return {
        "source_product": source_product,
        "target_product": target_product,
        "reason": reason
    }


def get_recommendations(product_name: str):
    driver = get_driver()

    with driver.session() as session:
        result = session.run(
            """
            MATCH (p:Product {name: $product_name})-[r:RECOMMENDS]->(rec:Product)
            RETURN rec.name AS name, rec.description AS description, r.reason AS reason
            """,
            product_name=product_name
        )

        return [
            {
                "name": record["name"],
                "description": record["description"],
                "reason": record["reason"]
            }
            for record in result
        ]
        
        
def create_relation(source_product: str, target_product: str, relation_type: str, reason: str):
    allowed_relations = {
        "RECOMMENDS",
        "HAS_SERVICE",
        "HAS_CARD",
        "INCLUDES",
        "ADAPTED_FOR",
        "RELATED_TO",
    }

    if relation_type not in allowed_relations:
        relation_type = "RELATED_TO"

    driver = get_driver()

    with driver.session() as session:
        session.run(
            f"""
            MERGE (source:Product {{name: $source_product}})
            MERGE (target:Product {{name: $target_product}})
            MERGE (source)-[r:{relation_type}]->(target)
            SET r.reason = $reason
            """,
            source_product=source_product,
            target_product=target_product,
            reason=reason,
        )

    return {
        "source_product": source_product,
        "target_product": target_product,
        "relation_type": relation_type,
        "reason": reason,
    }
    
    
def create_document(title: str, content_type: str):
    driver = get_driver()

    with driver.session() as session:
        session.run(
            """
            MERGE (d:Document {title: $title})
            SET d.content_type = $content_type
            """,
            title=title,
            content_type=content_type,
        )

    return {"title": title, "content_type": content_type}


def link_document_to_product(document_title: str, product_name: str):
    driver = get_driver()

    with driver.session() as session:
        session.run(
            """
            MERGE (d:Document {title: $document_title})
            MERGE (p:Product {name: $product_name})
            MERGE (d)-[:CONTAINS]->(p)
            """,
            document_title=document_title,
            product_name=product_name,
        )
