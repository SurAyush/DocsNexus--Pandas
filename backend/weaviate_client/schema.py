from weaviate_client.client import get_client
import weaviate.classes.config as wc

def create_article_schema():
    
    client = get_client()
    
    # Check if the class already exists, if not, create it
    if not client.collections.exists("Pandas_Reference_API"):
        client.collections.create(
            name="Pandas_Reference_API",
            properties=[
                wc.Property(name="api_id", data_type=wc.DataType.INT),
                wc.Property(name="name", data_type=wc.DataType.TEXT),
                wc.Property(name="file_path", data_type=wc.DataType.TEXT),
                wc.Property(name="function_signature", data_type=wc.DataType.TEXT),
                wc.Property(name="content", data_type=wc.DataType.TEXT),
                wc.Property(name="examples", data_type=wc.DataType.TEXT, multi_valued=True)
            ],
            vectorizer_config=None,  # No vectorization for this class
            description="A collection of Pandas API documentation articles",
        )

