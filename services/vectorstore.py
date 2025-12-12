# ========================================
# VECTORSTORE - services/vectorstore.py
# ========================================
# Base de datos vectorial usando ChromaDB
# Guarda vectores y permite buscar por similitud
# ========================================

# Importar ChromaDB (base de datos de vectores)
import chromadb
# Importar Settings para configuración avanzada
from chromadb.config import Settings
# Importar os para crear directorios
import os

# Crear la carpeta ./chroma si no existe
# exist_ok=True evita error si ya existe
os.makedirs("./chroma", exist_ok=True)

# Crear cliente de ChromaDB con persistencia local
# Los datos se guardan en ./chroma y persisten entre reinicios
client = chromadb.PersistentClient(path="./chroma")

# Obtener o crear la colección "documents"
# Una colección es como una tabla en una base de datos
collection = client.get_or_create_collection(
    name="documents",                    # Nombre de la colección
    metadata={"hnsw:space": "cosine"}    # Usar distancia coseno para similitud
                                         # (coseno mide el ángulo entre vectores)
)

def add_document_vectors(doc_id, title, chunks, embeddings):
    """
    Guarda los vectores de un documento en ChromaDB.
    
    Args:
        doc_id: ID único del documento
        title: Título del documento
        chunks: Lista de fragmentos de texto
        embeddings: Lista de vectores (uno por cada chunk)
    
    Ejemplo:
        doc_id = "abc-123"
        title = "Tutorial Python"
        chunks = ["Python es fácil", "Python es potente"]
        embeddings = [[0.1, 0.5, ...], [0.3, 0.2, ...]]
        add_document_vectors(doc_id, title, chunks, embeddings)
    """
    # Crear IDs únicos para cada chunk
    # Formato: "doc-id_0", "doc-id_1", etc.
    ids = [f"{doc_id}_{i}" for i in range(len(chunks))]

    # Agregar los chunks y sus vectores a ChromaDB
    collection.add(
        documents=chunks,        # Los textos originales
        embeddings=embeddings,   # Los vectores generados
        ids=ids,                 # IDs únicos para cada chunk
        metadatas=[{"doc_id": doc_id, "title": title} for _ in chunks]
                                # Metadatos (info adicional) de cada chunk
    )
    # ChromaDB guarda automáticamente cuando usas PersistentClient


def query_similar_chunks(query_embedding, top_k=3):
    """
    Busca los chunks más similares a una consulta.
    
    Args:
        query_embedding: Vector de la consulta del usuario
        top_k: Cuántos resultados devolver (por defecto 3)
    
    Returns:
        Diccionario con los resultados más similares:
        {
            "ids": [["doc1_0", "doc2_1", ...]],
            "documents": [["texto1", "texto2", ...]],
            "metadatas": [[{"doc_id": ..., "title": ...}, ...]],
            "distances": [[0.1, 0.3, ...]]  # Menor = más similar
        }
    """
    # Buscar en la colección
    return collection.query(
        query_embeddings=[query_embedding],  # Vector a buscar (en lista)
        n_results=top_k                      # Número de resultados
    )
    # ChromaDB devuelve los chunks ordenados por similitud (más similar primero)
