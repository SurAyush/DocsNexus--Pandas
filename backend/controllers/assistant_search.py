from controllers.search_query import search_query, rephrase_query
import generator_api as generator      # Uses Gemini-2.0-9B-it model (API key required)
# import generator        # For local LLM --> Phi-3-mini-4k-instruct


def assistant_search(query: str, topk: int = 5, alpha: float=0.5) -> dict:
    
    mod_query = rephrase_query(query)
    topk = min(topk, 5)  # Limit to a maximum of 5 results for efficiency
    alpha = min(max(alpha, 0), 1)  # Ensure alpha is between 0 and 1

    extracted_data = search_query(mod_query, topk=topk, alpha=alpha).get("result", [])
    
    data_string = "\n".join(extracted_data)
    if not data_string:
        return {"message": "No relevant results found."}
    else:
        output = generator.generate(query,data_string)
        return {"message": output}