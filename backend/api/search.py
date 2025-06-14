from fastapi import APIRouter
from controllers.search_query import search_query

router = APIRouter(
    prefix="/search",
)

@router.get("/semantic")
async def semantic_search(query: str, topk: int = 5, useRephraser: bool = True):
    """
    Perform semantic search on the Pandas Reference API using Weaviate.
    """
    return search_query(query, topk=topk, alpha=0, useRephraser=useRephraser)  

@router.get("/elastic")
async def elastic_search(query: str, topk: int = 5):
    """
    Perform elastic search on the Pandas Reference API using Weaviate.
    """
    return search_query(query, topk=topk, alpha=1.0, useRephraser=False)    # strict keyword matching

@router.get("/hybrid")
async def hybrid_search(query: str, topk: int = 5, alpha: float = 0.5, useRephraser: bool = True):
    """
    Perform hybrid search on the Pandas Reference API using Weaviate.
    """
    return search_query(query, topk=topk, alpha=0.5, useRephraser=useRephraser)