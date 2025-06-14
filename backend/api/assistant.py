from fastapi import APIRouter
from controllers.assistant_search import assistant_search

router = APIRouter()

@router.get("/")
async def assistant_generation(query: str, topk: int = 5, alpha: float = 0.5):
    return assistant_search(query=query, topk=topk, alpha=alpha)