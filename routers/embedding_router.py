# Endpoint POST /generate-embeddings. Busca un documento por ID, lo divide en chunks y genera/guarda sus vectores en ChromaDB. Maneja errores 404 si el documento no existe.
from fastapi import APIRouter, HTTPException, status
from models.schemas import EmbeddingInput, EmbeddingResponse
from services.store import get_document, get_all_documents
from services.chunker import chunk_text
from services.embeddings import embed_documents
from services.vectorstore import add_document_vectors

router = APIRouter()

@router.post("/generate-embeddings", response_model=EmbeddingResponse)

def generate_embeddings(data: EmbeddingInput):
    
    # Documento inexistente
    document = get_document(data.document_id)
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento no encontrado"
        )

    # Proceso controlado
    try:
        chunks = chunk_text(document["content"])
        embeddings = embed_documents(chunks)
        add_document_vectors(data.document_id, document["title"], chunks, embeddings)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="El servicio externo no pudo procesar la solicitud en este momento"
        )

    return {
        "message": "Embeddings generados exitosamente"
    }