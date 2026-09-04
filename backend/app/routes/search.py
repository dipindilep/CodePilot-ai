from fastapi import APIRouter, HTTPException

from backend.app.services.search_service import search_repository


router = APIRouter(
    prefix="/search",
    tags=["Search"]
)


@router.get("")
def search(
    path: str,
    query: str
):
    """
    Search for a query across the repository source files.
    """

    try:
        results = search_repository(path, query)

        return {
            "query": query,
            "results": results
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )