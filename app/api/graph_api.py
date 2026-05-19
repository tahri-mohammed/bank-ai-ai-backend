from fastapi import APIRouter
from pydantic import BaseModel

from app.graph.graph_service import (
    create_product,
    create_recommendation,
    get_recommendations
)

router = APIRouter(prefix="/api/graph", tags=["Graph"])


class ProductRequest(BaseModel):
    name: str
    description: str


class RecommendationRequest(BaseModel):
    source_product: str
    target_product: str
    reason: str


@router.post("/products")
def add_product(request: ProductRequest):
    return create_product(request.name, request.description)


@router.post("/recommendations")
def add_recommendation(request: RecommendationRequest):
    return create_recommendation(
        request.source_product,
        request.target_product,
        request.reason
    )


@router.get("/recommendations/{product_name}")
def recommendations(product_name: str):
    return get_recommendations(product_name)
