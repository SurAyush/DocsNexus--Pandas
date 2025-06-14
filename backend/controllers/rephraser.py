import generator_api as generator

def rephrase_query(user_query: str) -> str:
    """Given an input query to the model, it will return the query helpful for semantic search"""

    return generator.remake_query(user_query)