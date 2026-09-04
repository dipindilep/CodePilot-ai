from fastapi import FastAPI

from backend.app.routes.chat import router as chat_router
from backend.app.routes.repository import router as repository_router
from backend.app.routes.search import router as search_router

app = FastAPI(
    title="CodePilot AI",
    description="A local AI software engineering assistant",
    version="0.1.0"
)

app.include_router(chat_router)
app.include_router(repository_router)
app.include_router(search_router)

@app.get("/")
def root():
    return {
        "message": "Welcome to CodePilot AI!"
    }