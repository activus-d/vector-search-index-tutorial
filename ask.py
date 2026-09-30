import ollama

from config import VECTOR_INDEX_NAME
from db import get_collection
from embeddings import embed_query

OLLAMA_MODEL = "llama3.2:3b"
NUM_CANDIDATES_MULTIPLIER = 20
RESULT_LIMIT = 5


def retrieve(question):
    collection = get_collection()
    query_vector = embed_query(question)

    pipeline = [
        {
            "$vectorSearch": {
                "index": VECTOR_INDEX_NAME,
                "path": "embedding",
                "queryVector": query_vector,
                "numCandidates": RESULT_LIMIT * NUM_CANDIDATES_MULTIPLIER,
                "limit": RESULT_LIMIT,
            }
        },
        {"$project": {"_id": 0, "text": 1, "source_file": 1, "chunk_index": 1}},
    ]

    return list(collection.aggregate(pipeline))


def build_prompt(question, chunks):
    ordered = sorted(chunks, key=lambda chunk: (chunk["source_file"], chunk["chunk_index"]))
    context = "\n\n".join(
        f"[{chunk['source_file']}, chunk {chunk['chunk_index']}]\n{chunk['text']}"
        for chunk in ordered
    )
    return (
        "Answer the question using only the context below. "
        "If the context doesn't contain the answer, say so.\n\n"
        f"Context:\n{context}\n\nQuestion: {question}"
    )


def ask(question):
    chunks = retrieve(question)
    prompt = build_prompt(question, chunks)

    response = ollama.chat(
        model=OLLAMA_MODEL,
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": 0},
    )
    answer = response["message"]["content"]

    citations = [f"{chunk['source_file']} (chunk {chunk['chunk_index']})" for chunk in chunks]
    return answer, citations


def main():
    print("Ask a question about your documents. Type 'quit' to exit.\n")
    while True:
        question = input("> ").strip()
        if question.lower() in ("quit", ""):
            break

        answer, citations = ask(question)
        print(f"\n{answer}\n")
        print("Sources:")
        for citation in citations:
            print(f"  - {citation}")
        print()


if __name__ == "__main__":
    main()