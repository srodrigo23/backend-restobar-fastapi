from fastapi import FastAPI
from routes import products_router

app = FastAPI()

@app.on_event("startup")
def on_startup():
    """Startup event handler to create database and tables."""
    from database import create_db_and_tables
    create_db_and_tables()

# Include routers
app.include_router(products_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}
