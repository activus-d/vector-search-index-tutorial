import time

from pymongo.operations import SearchIndexModel

from config import EMBEDDING_DIMENSIONS, VECTOR_INDEX_NAME
from db import get_collection


def create_vector_index():
    collection = get_collection()

    search_index_model = SearchIndexModel(
        definition={
            "fields": [
                {
                    "type": "vector",
                    "path": "embedding",
                    "numDimensions": EMBEDDING_DIMENSIONS,
                    "similarity": "dotProduct",
                    "quantization": "scalar",
                },
                {
                    "type": "filter",
                    "path": "source_file",
                },
            ]
        },
        name=VECTOR_INDEX_NAME,
        type="vectorSearch",
    )

    result = collection.create_search_index(model=search_index_model)
    print(f"Creating index '{result}'. Waiting for it to become queryable...")

    while True:
        indexes = list(collection.list_search_indexes(result))
        if indexes and indexes[0].get("queryable"):
            break
        time.sleep(5)

    print(f"Index '{result}' is ready to query.")


if __name__ == "__main__":
    create_vector_index()