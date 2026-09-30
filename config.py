import os

from dotenv import load_dotenv

load_dotenv()

APP_NAME = "devrel-tutorial-python-vectorsearch-repo"
MONGODB_URI = os.environ["MONGODB_URI"]
VOYAGE_API_KEY = os.environ["VOYAGE_API_KEY"]

DATABASE_NAME = "document_insights"
COLLECTION_NAME = "chunks"
EMBEDDING_MODEL = "voyage-4"
EMBEDDING_DIMENSIONS = 1024
VECTOR_INDEX_NAME = "vector_index"