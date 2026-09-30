from functools import cache

from pymongo import MongoClient

from config import APP_NAME, COLLECTION_NAME, DATABASE_NAME, MONGODB_URI


@cache
def get_client():
    return MongoClient(MONGODB_URI, appname=APP_NAME)


def get_collection():
    client = get_client()
    return client[DATABASE_NAME][COLLECTION_NAME]

def save_chunks(filename, chunks, embeddings):
    collection = get_collection()
    for index, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        collection.update_one(
            {"source_file": filename, "chunk_index": index},
            {
                "$set": {
                    "source_file": filename,
                    "chunk_index": index,
                    "text": chunk,
                    "embedding": embedding,
                }
            },
            upsert=True,
        )
    collection.delete_many({"source_file": filename, "chunk_index": {"$gte": len(chunks)}})