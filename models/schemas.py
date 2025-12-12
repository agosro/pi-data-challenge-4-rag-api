# ========================================
# SCHEMAS - models/schemas.py
# ========================================
# Define los MODELOS DE DATOS usando Pydantic
# Valida automáticamente que los datos tengan el formato correcto
# ========================================

# Importar BaseModel de Pydantic (base para crear modelos de datos)
from pydantic import BaseModel
# Importar tipos para listas y valores opcionales
from typing import List, Optional

# ========== MODELOS DE ENTRADA (REQUEST) ==========
# Estos definen qué datos debe enviar el cliente

class UploadInput(BaseModel):
    """
    Modelo para subir un documento.
    El cliente debe enviar título y contenido.
    """
    title: str      # Título del documento (tipo texto)
    content: str    # Contenido del documento (tipo texto)

class EmbeddingInput(BaseModel):
    """
    Modelo para generar embeddings de un documento.
    Solo necesita el ID del documento.
    """
    document_id: str  # ID único del documento (UUID)

class SearchInput(BaseModel):
    """
    Modelo para buscar documentos.
    El usuario envía una consulta en texto.
    """
    query: str  # Texto de búsqueda

class AskInput(BaseModel):
    """
    Modelo para hacer una pregunta al sistema.
    El usuario envía su pregunta.
    """
    question: str  # Pregunta del usuario


# ========== MODELOS DE SALIDA (RESPONSE) ==========
# Estos definen qué datos devuelve el servidor

class UploadResponse(BaseModel):
    """
    Respuesta después de subir un documento.
    Incluye mensaje de éxito y el ID generado.
    """
    message: str        # Mensaje de confirmación
    document_id: str    # ID del documento creado

class EmbeddingResponse(BaseModel):
    """
    Respuesta después de generar embeddings.
    Solo incluye mensaje de confirmación.
    """
    message: str  # Mensaje de confirmación

class SearchResult(BaseModel):
    """
    Un resultado individual de búsqueda.
    Contiene información del documento encontrado.
    """
    document_id: str        # ID del documento
    title: str              # Título del documento
    content_snippet: str    # Fragmento del contenido (preview)
    similarity_score: float # Qué tan similar es (0.0 a 1.0)

class SearchResponse(BaseModel):
    """
    Respuesta completa de búsqueda.
    Contiene una lista de resultados.
    """
    results: List[SearchResult]  # Lista de resultados (puede estar vacía)

class AskResponse(BaseModel):
    """
    Respuesta a una pregunta del usuario.
    Incluye la respuesta generada y metadatos.
    """
    question: str                    # La pregunta original
    answer: str                      # La respuesta generada
    grounded: bool                   # Si la respuesta está basada en documentos
    context_used: Optional[str]      # Contexto usado (puede ser None)
    similarity_score: Optional[float] # Score de similitud (puede ser None)
