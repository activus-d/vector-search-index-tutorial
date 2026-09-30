from config import VECTOR_INDEX_NAME
from db import get_collection
from embeddings import embed_query

NUM_CANDIDATES_MULTIPLIER = 20


def search(question, limit=5):
    collection = get_collection()
    query_vector = embed_query(question)

    pipeline = [
        {
            "$vectorSearch": {
                "index": VECTOR_INDEX_NAME,
                "path": "embedding",
                "queryVector": query_vector,
                "numCandidates": limit * NUM_CANDIDATES_MULTIPLIER,
                "limit": limit,
            }
        },
        {
            "$project": {
                "_id": 0,
                "text": 1,
                "source_file": 1,
                "chunk_index": 1,
                "score": {"$meta": "vectorSearchScore"},
            }
        },
    ]

    return list(collection.aggregate(pipeline))


if __name__ == "__main__":
    for result in search("What unalienable rights does the Declaration list?"):
        print(f"{result['source_file']} (chunk {result['chunk_index']}, score {result['score']:.3f})")
        print(result["text"][:200])
        print()