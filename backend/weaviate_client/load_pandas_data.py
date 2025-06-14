from weaviate_client.client import get_client
from weaviate_client.schema import create_article_schema
from datasets import load_dataset

# Load articles in form of batches
def load_articles():

    create_article_schema()
    client = get_client()

    dataset = load_dataset("SurAyush/Pandas_Docs_embedding")
    articles = dataset["train"]
    print("Articles loaded successfully.")
    print(f"Number of articles: {len(articles)}")

    collection = client.collections.get("Pandas_Reference_API")
    
    print(collection.aggregate.over_all(total_count=True).total_count)
    
    with collection.batch.fixed_size(batch_size=100) as batch:
        
        for article in articles:
            data = {
                "api_id": article["id"],
                "file_path": article["file_path"],
                "function_signature": article["function_signature"],
                "content": article["content"],
                "parameters": article["parameters"],
                "examples": article["examples"]
            }
            batch.add_object(
                properties=data,
                vector=article.get("embeddings",None)
            )

    
    failed_objects = collection.batch.failed_objects
    if failed_objects:
        print(f"Number of failed imports: {len(failed_objects)}")
        print(f"First failed object: {failed_objects[0]}")
    else:
        print("All articles loaded successfully.")

    print(collection.aggregate.over_all(total_count=True).total_count)



print("Articles loading initiated.")
if __name__ == "__main__":
    load_articles()
