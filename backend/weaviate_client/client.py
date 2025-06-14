import weaviate

client = weaviate.connect_to_custom(
    http_host="localhost",
    grpc_host="localhost",
    http_port=8080,
    grpc_port=50051,
    grpc_secure=False,
    http_secure=False,
)

def get_client():
    return client