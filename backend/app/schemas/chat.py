from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str
    project_path: str | None = None


class ChatResponse(BaseModel):
    answer: str