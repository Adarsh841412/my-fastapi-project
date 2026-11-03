from fastapi import FastAPI 
from app.api.v1.router import api_router 


app = FastAPI(
    title="Secure Auth FastAPI Project",
    description="A modular authentication system built with FastAPI, SQLAlchemy, and Pydantic.",
    version="1.0.0"
)


app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def root():
    return {
        "message": "Welcome to the API!",
        "docs": "Go to /docs or /redoc to test your endpoints interactively."
    }