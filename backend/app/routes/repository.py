from fastapi import APIRouter, HTTPException

from backend.app.services.repository_service import (
    list_source_files,
    read_file_content,
)

router = APIRouter(prefix="/repository", tags=["Repository"])

@router.get("/files")
def get_source_files(path: str):
    """
    Return all supported source files in a project.
    """
    try:
        files = list_source_files(path)
        return {"files": files}

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.get("/file")
def get_file_content(path: str):
    """
    Return the content of a source file.
    """
    try:
        content = read_file_content(path)
        return {"content": content}

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )