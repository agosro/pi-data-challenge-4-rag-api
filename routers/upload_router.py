from fastapi import APIRouter, HTTPException, status
from models.schemas import UploadInput, UploadResponse
from services.store import save_document

router = APIRouter()

@router.post("/upload", response_model=UploadResponse, status_code=status.HTTP_201_CREATED)

def upload_document(data: UploadInput):

    # Validaciones de entrada
    if not data.title.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El título no puede estar vacío"
        )

    if not data.content.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El contenido no puede estar vacío"
        )

    # Guardado seguro
    try:
        doc_id = save_document(data.title, data.content)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudo procesar la solicitud en este momento"
        )

    return {
        "message": "Documento subido con éxito",
        "document_id": doc_id
    }