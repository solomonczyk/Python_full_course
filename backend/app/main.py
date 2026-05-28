from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import init_db
from app.routers import lessons, progress, quiz

app = FastAPI(
    title="Python Quest API",
    description="Backend for the Python Quest interactive learning course",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
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
