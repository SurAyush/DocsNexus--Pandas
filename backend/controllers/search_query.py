from weaviate_client.client import get_client
import vectorizer
from controllers.rephraser import rephrase_query
from controllers.reranker import rerank

def search_query(query: str, topk: int = 5, alpha: float = 0.5, useRephraser: bool = True, useReranker: bool = True) -> dict:

    client = get_client()
    connection = client.collections.get("Pandas_Reference_API")
    query = rephrase_query(query) if useRephraser else query

    embedding = vectorizer.get_embeddings([query])[0].tolist()

    topk = min(topk, 5)     # capping topk to 5 for performance reasons
    
    result = connection.query.hybrid(
        query=query,
        vector=embedding, 
        alpha=alpha,
        limit=topk*10 if useReranker else topk,
        return_properties=["function_signature", "content", "parameters"],
    )

    items = result.objects    

    extracted_data = [
        f"""
        {i+1}. {item.properties.get("function_signature")}
        Description: {item.properties.get("content")}
        """
        
        for i, item in enumerate(items[:topk])
        if item.properties and "function_signature" in item.properties
    ]

    top_k_reranked = rerank(query, extracted_data, topk) if useReranker else extracted_data

    return {
        "result": top_k_reranked if extracted_data else "No relevant results found."
    }