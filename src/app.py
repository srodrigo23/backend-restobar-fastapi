from typing import Annotated
from database import SessionDep, Product, ProductCreate, ProductPublic
from fastapi import FastAPI, Query

from sqlmodel import select

app = FastAPI()

@app.on_event("startup")
def on_startup():
    """Startup event handler to create database and tables."""
    from database import create_db_and_tables
    create_db_and_tables()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/products", response_model=list[ProductPublic])
def get_products(
    session:SessionDep,
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

@app.get("/products/{product_id}", response_model=ProductPublic)
def get_product(
    product_id: int,
    session: SessionDep
) -> ProductPublic | None:
    """Get a product by its ID."""
    
    return session.exec(
        select(Product).where(Product.id == product_id)
    ).one_or_none()

@app.post("/products", response_model=ProductPublic)
def create_product(
    product: ProductCreate,
    session: SessionDep
):
    """Create a new product."""

    db_prodcut = Product.model_validate(product)
    session.add(db_prodcut)
    session.commit()
    session.refresh(db_prodcut)
    return db_prodcut
