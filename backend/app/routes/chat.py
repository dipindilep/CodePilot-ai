
from pathlib import Path

from fastapi import APIRouter, HTTPException

from backend.app.schemas.chat import ChatRequest, ChatResponse
from backend.app.services.ollama_service import generate_response
from rag.indexer import project_collection_name, index_project
from rag.retriever import CodeRetriever
from rag.context_builder import build_context

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    context = ""

    if request.project_path:
        project_path = Path(request.project_path).expanduser().resolve()

        if not project_path.is_dir():
            raise HTTPException(
                status_code=400,
                detail="The selected project directory does not exist.",
            )

        collection_name = project_collection_name(project_path)

        try:
            index_project(
                project_path,
                reset=False,
            )

            retriever = CodeRetriever(collection_name)
            chunks = retriever.retrieve(request.message, n_results=5)
            context = build_context(chunks)

        except Exception as exc:
            raise HTTPException(
                status_code=500,
                detail=f"Could not search the selected project: {exc}",
            ) from exc

    answer = generate_response(request.message, context=context)

    return ChatResponse(answer=answer)
