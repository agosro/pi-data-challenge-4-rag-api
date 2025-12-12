# ========================================
# UPLOAD ROUTER - routers/upload_router.py
# ========================================
# Endpoint POST /upload
# Permite al usuario subir documentos al sistema
# ========================================

# Importar componentes de FastAPI
from fastapi import APIRouter, HTTPException, status
# Importar los modelos de datos para este endpoint
from models.schemas import UploadInput, UploadResponse
# Importar la función para guardar documentos
from services.store import save_document

# Crear un router (grupo de endpoints relacionados)
router = APIRouter()

# Decorador que define el endpoint POST /upload
# response_model: qué tipo de respuesta devuelve
# status_code: código HTTP cuando todo sale bien (201 = Created)
@router.post("/upload", response_model=UploadResponse, status_code=status.HTTP_201_CREATED)
def upload_document(data: UploadInput):
    """
    Endpoint para subir un nuevo documento.
    
    Args:
        data: Objeto con title y content (validado por Pydantic)
    
    Returns:
        Diccionario con mensaje y document_id
    
    Raises:
        HTTPException 400: Si título o contenido están vacíos
        HTTPException 500: Si hay un error al guardar
    """

    # Validación 1: Verificar que el título no esté vacío
    # .strip() elimina espacios al inicio/fin
    if not data.title.strip():
        # Lanzar excepción con código 400 (Bad Request)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El título no puede estar vacío"
        )

    # Validación 2: Verificar que el contenido no esté vacío
    if not data.content.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El contenido no puede estar vacío"
        )

    # Intentar guardar el documento
    # El bloque try-except captura cualquier error
    try:
        # Llamar a save_document y obtener el ID generado
        doc_id = save_document(data.title, data.content)
    except Exception:
        # Si algo sale mal, devolver error 500
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudo procesar la solicitud en este momento"
        )

    # Devolver respuesta exitosa
    # FastAPI la convierte automáticamente a JSON
    return {
        "message": "Documento subido con éxito",
        "document_id": doc_id
    }