from config import EMBEDDING_DIMENSIONS, VECTOR_INDEX_NAME
from db import get_collection


def update_quantization(quantization="none"):
    collection = get_collection()
    definition = {
        "fields": [
            {
                "type": "vector",
                "path": "embedding",
                "numDimensions": EMBEDDING_DIMENSIONS,
                "similarity": "dotProduct",
                "quantization": quantization,
            },
            {"type": "filter", "path": "source_file"},
        ]
    }
    collection.update_search_index(VECTOR_INDEX_NAME, definition)
    print(f"Updated '{VECTOR_INDEX_NAME}' to use quantization='{quantization}'.")


def show_index_status():
    collection = get_collection()
    for index in collection.list_search_indexes():
        print(f"{index['name']}: status={index['status']}, queryable={index['queryable']}")


def delete_index():
    collection = get_collection()
    collection.drop_search_index(VECTOR_INDEX_NAME)
    print(f"Deleted '{VECTOR_INDEX_NAME}'.")


if __name__ == "__main__":
    show_index_status()