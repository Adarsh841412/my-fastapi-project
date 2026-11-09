from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.router import api_router 
from app.Exceptions.auth_exceptions import InvalidCredentialException, EmailAlreadyExistException
from app.core.api_config import API_PREFIX

app = FastAPI(
    title="Secure Auth FastAPI Project",
    description="A modular authentication system built with FastAPI, SQLAlchemy, and Pydantic.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(InvalidCredentialException)
async def invalid_credential_handler(request: Request, exc: InvalidCredentialException):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": exc.msg},
        headers={"WWW-Authenticate": "Bearer"},
    )


@app.exception_handler(EmailAlreadyExistException)
async def email_exist_exception(request: Request, exc: EmailAlreadyExistException):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": exc.msg},
    )

app.include_router(api_router, prefix=API_PREFIX)
@app.get("/")
def root():
    return {
        "message": "Welcome to the API!",
        "docs": "Go to /docs or /redoc to test your endpoints interactively."
    }