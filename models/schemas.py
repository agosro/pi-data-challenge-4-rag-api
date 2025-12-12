# Define las estructuras de datos (Input/Output) usando Pydantic. Asegura que los datos que entran y salen de la API tengan el formato correcto (ej: que UploadInput tenga título y contenido).
from pydantic import BaseModel
from typing import List, Optional

# ---------- INPUTS ----------

class UploadInput(BaseModel):
    title: str
    content: str

class EmbeddingInput(BaseModel):
    document_id: str

class SearchInput(BaseModel):
    query: str

class AskInput(BaseModel):
    question: str


# ---------- OUTPUTS ----------

class UploadResponse(BaseModel):
    message: str
    document_id: str

class EmbeddingResponse(BaseModel):
    message: str

class SearchResult(BaseModel):
    document_id: str
    title: str
    content_snippet: str
    similarity_score: float

class SearchResponse(BaseModel):
    results: List[SearchResult]

class AskResponse(BaseModel):
    question: str
    answer: str
    grounded: bool
    context_used: Optional[str]
    similarity_score: Optional[float]
