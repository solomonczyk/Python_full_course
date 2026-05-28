import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import init_db
from app.routers import lessons, progress, quiz

app = FastAPI(
    title="Python Quest API",
    description="Backend for the Python Quest interactive learning course",
    version="1.0.0",
)

_extra_origin = os.environ.get("ALLOWED_ORIGIN", "")
_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    *([_extra_origin] if _extra_origin else []),
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins,
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(lessons.router)
app.include_router(progress.router)
app.include_router(quiz.router)


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/")
def root() -> dict[str, str]:
    return {"status": "ok", "app": "Python Quest API"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy"}
