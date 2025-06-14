from weaviate_client.client import get_client
import vectorizer
from controllers.rephraser import rephrase_query

def search_query(query: str, topk: int = 5, alpha: float = 0.5, useRephraser: bool = True) -> dict:

    client = get_client()
    connection = client.collections.get("Pandas_Reference_API")
    query = rephrase_query(query) if useRephraser else query

    embedding = vectorizer.get_embeddings([query])[0].tolist()
    
    result = connection.query.hybrid(
        query=query,
        vector=embedding, 
        alpha=0,
        return_properties=["function_signature", "content", "parameters"],
    )

    items = result.objects  
    topk = min(topk, len(items))  
    extracted_data = [
        f"""
        {i+1}. {item.properties.get("function_signature")}
        Description: {item.properties.get("content")}
        """
        
        for i, item in enumerate(items[:topk])
        if item.properties and "function_signature" in item.properties
    ]

    return {
        "result": extracted_data if extracted_data else "No relevant results found."
    }