from fastapi import APIRouter, HTTPException, status
from models.schemas import SearchInput, SearchResponse
from services.search import semantic_search
from services.logging import logger

router = APIRouter()

@router.post("/search", response_model=SearchResponse, status_code=status.HTTP_200_OK)

def search_documents(data: SearchInput):
    
    # Validación de entrada
    if not data.query.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La consulta no puede estar vacía"
        )
    
    logger.info("SEARCH | start | query_len=%s", len(data.query))

    # Búsqueda controlada
    try:
        results = semantic_search(data.query)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="El servicio externo no pudo procesar la solicitud en este momento"
        )
    
    logger.info("SEARCH | success | results_count=%s", len(results))

    # Respuesta válida aunque no haya resultados
    return {
        "results": results
    }