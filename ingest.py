import os

from db import save_chunks
from embeddings import embed_documents

SAMPLE_DOCS_DIR = "sample_documents"
CHUNK_SIZE = 900


def chunk_text(text):
    paragraphs = [paragraph.strip() for paragraph in text.split("\n\n") if paragraph.strip()]
    chunks = []
    current = ""
    for paragraph in paragraphs:
        if current and len(current) + len(paragraph) + 2 > CHUNK_SIZE:
            chunks.append(current)
            current = paragraph
        else:
            current = f"{current}\n\n{paragraph}" if current else paragraph
    if current:
        chunks.append(current)
    return chunks


def ingest_documents():
    for filename in sorted(os.listdir(SAMPLE_DOCS_DIR)):
        if not filename.endswith(".txt"):
            continue

        path = os.path.join(SAMPLE_DOCS_DIR, filename)
        with open(path, encoding="utf-8") as file:
            text = file.read()

        chunks = chunk_text(text)
        embeddings = embed_documents(chunks)
        save_chunks(filename, chunks, embeddings)
        print(f"Ingested {len(chunks)} chunks from {filename}.")


if __name__ == "__main__":
    ingest_documents()