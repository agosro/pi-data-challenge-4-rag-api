# ========================================
# SEARCH - services/search.py
# ========================================
# Coordina la búsqueda semántica
# Convierte consultas en vectores y busca documentos similares
# ========================================

# Importar la función para generar embeddings de consultas
from services.embeddings import embed_query
# Importar la función para buscar en ChromaDB
from services.vectorstore import query_similar_chunks

def semantic_search(query: str, top_k: int = 3) -> list[dict]:
    """
    Realiza una búsqueda semántica sobre los documentos.
    
    Args:
        query: La consulta del usuario (texto)
        top_k: Número de resultados a devolver (por defecto 3)
    
    Returns:
        Lista de diccionarios con los resultados:
        [
            {
                "document_id": "abc-123",
                "title": "Tutorial Python",
                "content_snippet": "Python es fácil...",
                "similarity_score": 0.95
            },
            ...
        ]
    """
    # Paso 1: Convertir la consulta en un vector
    query_vec = embed_query(query)
    
    # Paso 2: Buscar los chunks más similares en ChromaDB
    results = query_similar_chunks(query_vec, top_k)

    # Paso 3: Formatear los resultados para la respuesta
    output = []
    # Iterar sobre cada resultado encontrado
    for i in range(len(results["ids"][0])):
        # Obtener la distancia (menor = más similar)
        distance = float(results["distances"][0][i])
        
        # Convertir distancia a score de similitud (0.0 a 1.0)
        # Formula: similarity = 1 - distance
        # max/min aseguran que esté entre 0 y 1
        similarity_score = max(0.0, min(1.0, 1.0 - distance))

        # Crear el diccionario de resultado
        output.append({
            "document_id": results["metadatas"][0][i]["doc_id"],  # ID del documento
            "title": results["metadatas"][0][i]["title"],         # Título
            "content_snippet": results["documents"][0][i][:150] + "...",  # Primeros 150 caracteres
            "similarity_score": similarity_score                  # Score calculado
        })

    # Devolver la lista de resultados
    return output
