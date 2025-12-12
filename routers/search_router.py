# ========================================
# SEARCH ROUTER - routers/search_router.py
# ========================================
# Endpoint POST /search
# Busca documentos similares a una consulta
# ========================================

# Importar componentes de FastAPI
from fastapi import APIRouter, HTTPException, status
# Importar modelos de datos
from models.schemas import SearchInput, SearchResponse
# Importar función de búsqueda semántica
from services.search import semantic_search
# Importar logger para registrar eventos
from services.logging import logger

# Crear el router
router = APIRouter()

# Decorador para definir el endpoint POST /search
@router.post("/search", response_model=SearchResponse, status_code=status.HTTP_200_OK)
def search_documents(data: SearchInput):
    """
    Busca documentos similares a una consulta del usuario.
    
    Args:
        data: Objeto con query (consulta de texto)
    
    Returns:
        Lista de resultados con documentos similares
    
    Raises:
        HTTPException 400: Si la consulta está vacía
        HTTPException 500: Si falla la búsqueda
    """
    
    # Validación: Verificar que la consulta no esté vacía
    if not data.query.strip():
        # Devolver error 400 si está vacía
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La consulta no puede estar vacía"
        )
    
    # Registrar en el log que inició la búsqueda
    # %s se reemplaza por el segundo argumento (len(data.query))
    logger.info("SEARCH | start | query_len=%s", len(data.query))

    # Intentar realizar la búsqueda
    try:
        # Llamar a la función de búsqueda semántica
        # Esta convierte la query en vector y busca en ChromaDB
        results = semantic_search(data.query)
    except Exception:
        # Si algo falla (API de Cohere, ChromaDB, etc.), devolver error 500
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="El servicio externo no pudo procesar la solicitud en este momento"
        )
    
    # Registrar en el log que la búsqueda fue exitosa
    logger.info("SEARCH | success | results_count=%s", len(results))

    # Devolver los resultados
    # Incluso si results está vacía ([]), es una respuesta válida
    return {
        "results": results
    }