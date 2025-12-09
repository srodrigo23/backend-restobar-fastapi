from typing import Annotated
from fastapi import APIRouter, Query
from sqlmodel import select

from database import SessionDep, Product, ProductCreate, ProductPublic

router = APIRouter(
    prefix="/products",
    tags=["products"]
)

@router.get("", response_model=list[ProductPublic])
def get_products(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100
) -> list[ProductPublic]:
    """
    Get a list of products with pagination.
    - `offset`: The number of products to skip.
    - `limit`: The maximum number of products to return (default is 100, max is 100).
    """
    if limit > 100:
        raise ValueError("Limit cannot exceed 100.")
    if offset < 0:
        raise ValueError("Offset cannot be negative.")
    return session.exec(
        select(Product).offset(offset).limit(limit)
    ).all()

@router.get("/{product_id}", response_model=ProductPublic)
def get_product(
    product_id: int,
    session: SessionDep
) -> ProductPublic | None:
    """Get a product by its ID."""

    return session.exec(
        select(Product).where(Product.id == product_id)
    ).one_or_none()

@router.post("", response_model=ProductPublic)
def create_product(
    product: ProductCreate,
    session: SessionDep
) -> ProductPublic:
    """Create a new product."""

    db_product = Product.model_validate(product)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product
