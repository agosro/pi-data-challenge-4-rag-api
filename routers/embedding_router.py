# ========================================
# EMBEDDING ROUTER - routers/embedding_router.py
# ========================================
# Endpoint POST /generate-embeddings
# Genera vectores de un documento y los guarda en ChromaDB
# ========================================

# Importar componentes de FastAPI
from fastapi import APIRouter, HTTPException, status
# Importar modelos de datos
from models.schemas import EmbeddingInput, EmbeddingResponse
# Importar función para obtener documentos
from services.store import get_document, get_all_documents
# Importar función para dividir en chunks
from services.chunker import chunk_text
# Importar función para generar embeddings
from services.embeddings import embed_documents
# Importar función para guardar en ChromaDB
from services.vectorstore import add_document_vectors

# Crear el router
router = APIRouter()

# Decorador para definir el endpoint POST /generate-embeddings
@router.post("/generate-embeddings", response_model=EmbeddingResponse)
def generate_embeddings(data: EmbeddingInput):
    """
    Genera embeddings para un documento y los guarda en ChromaDB.
    
    Este endpoint realiza 3 pasos:
    1. Divide el documento en chunks (fragmentos)
    2. Genera un vector para cada chunk
    3. Guarda los vectores en ChromaDB
    
    Args:
        data: Objeto con document_id
    
    Returns:
        Mensaje de confirmación
    
    Raises:
        HTTPException 404: Si el documento no existe
        HTTPException 500: Si falla la generación o guardado
    """
    
    # Paso 1: Buscar el documento por ID
    document = get_document(data.document_id)
    
    # Verificar si el documento existe
    if not document:
        # Si no existe, devolver error 404 (Not Found)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento no encontrado"
        )

    # Paso 2, 3 y 4: Procesar el documento
    # Envolver en try-except para capturar errores
    try:
        # Paso 2: Dividir el contenido en chunks
        chunks = chunk_text(document["content"])
        
        # Paso 3: Generar embeddings para cada chunk
        # Esto llama a la API de Cohere
        embeddings = embed_documents(chunks)
        
        # Paso 4: Guardar chunks y embeddings en ChromaDB
        add_document_vectors(data.document_id, document["title"], chunks, embeddings)
        
    except Exception:
        # Si algo falla (API de Cohere, ChromaDB, etc.), devolver error 500
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="El servicio externo no pudo procesar la solicitud en este momento"
        )

    # Devolver respuesta exitosa
    return {
        "message": "Embeddings generados exitosamente"
    }