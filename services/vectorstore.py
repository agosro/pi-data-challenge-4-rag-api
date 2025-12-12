import chromadb
from chromadb.config import Settings
import os

# Crear carpeta si no existe
os.makedirs("./chroma", exist_ok=True)

# Persistencia local
client = chromadb.PersistentClient(path="./chroma")

# Creamos o recuperamos la colección
collection = client.get_or_create_collection(
    name="documents",
    metadata={"hnsw:space": "cosine"}
)

def add_document_vectors(doc_id, title, chunks, embeddings):
    ids = [f"{doc_id}_{i}" for i in range(len(chunks))]

    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=ids,
        metadatas=[{"doc_id": doc_id, "title": title} for _ in chunks]
    )


def query_similar_chunks(query_embedding, top_k=3):
    return collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
