import time

import voyageai

from config import EMBEDDING_MODEL, VOYAGE_API_KEY

vo = voyageai.Client(api_key=VOYAGE_API_KEY)

BATCH_SIZE = 30
SECONDS_BETWEEN_CALLS = 21


def embed_documents(texts):
    embeddings = []
    for start in range(0, len(texts), BATCH_SIZE):
        batch = texts[start : start + BATCH_SIZE]
        result = vo.embed(batch, model=EMBEDDING_MODEL, input_type="document")
        embeddings.extend(result.embeddings)
        time.sleep(SECONDS_BETWEEN_CALLS)
    return embeddings


def embed_query(text):
    result = vo.embed([text], model=EMBEDDING_MODEL, input_type="query")
    return result.embeddings[0]