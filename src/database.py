from typing import Annotated

from fastapi import Depends
from sqlmodel import SQLModel, Field
from sqlmodel import Field, Session, SQLModel, create_engine, select

class ProductBase(SQLModel):
    """Base model for Product."""
    name: str = Field(max_length=100)
    description: str | None = Field(default=None, max_length=500)

class Product(ProductBase, table=True):
    """Product model for the database."""
    id: int   | None = Field(default=None, primary_key=True)

class ProductCreate(Product):
    """Product creation modeldsd."""
    price: float | None = Field(default=None, ge=0)
    stock: int | None = Field(default=None, ge=0)

class ProductPublic(ProductBase):
    """Public model for Product."""
    id: int


class Order(SQLModel, table=True):
    """Order model for the database."""
    id: int | None = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="product.id")
    quantity: int = Field(ge=1)

    class Config:
        orm_mode = True


sqlite_file_name = "database.db"
sqlite_database_url = f"sqlite:///.{sqlite_file_name}"


def create_db_and_tables():
    """Create the database and tables."""

    engine = create_engine(
        sqlite_database_url, 
        echo=True, 
        connect_args={
            "check_same_thread": False
        }
    )
    SQLModel.metadata.create_all(engine)
    print("Database and tables created successfully.")

def get_session():
    """Get a database session."""

    engine = create_engine(
        sqlite_database_url, 
        echo=True, 
        connect_args={
            "check_same_thread": False
        }
    )
    # return Session(engine)
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session), "Database session dependency"]