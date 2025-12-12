# ========================================
# ASK ROUTER - routers/ask_router.py
# ========================================
# Endpoint POST /ask
# Responde preguntas usando RAG (Retrieval Augmented Generation)
# ========================================

# Importar componentes de FastAPI
from fastapi import APIRouter, HTTPException, status
# Importar modelos de datos
from models.schemas import AskInput, AskResponse
# Importar función para responder preguntas con LLM
from services.llm import answer_question
# Importar filtro de moderación de contenido
from services.moderation import contains_inappropriate_language
# Importar logger para registrar eventos
from services.logging import logger

# Crear el router
router = APIRouter()

# Decorador para definir el endpoint POST /ask
@router.post("/ask", response_model=AskResponse, status_code=status.HTTP_200_OK)
def ask_question(data: AskInput):
    """
    Responde preguntas del usuario usando RAG con grounding.
    
    Proceso:
    1. Valida que la pregunta no esté vacía
    2. Verifica que no contenga lenguaje inapropiado
    3. Busca contexto relevante en documentos
    4. Genera respuesta usando LLM
    
    Args:
        data: Objeto con question (pregunta del usuario)
    
    Returns:
        Respuesta con answer, grounded, context_used, similarity_score
    
    Raises:
        HTTPException 400: Si la pregunta está vacía
        HTTPException 500: Si falla la generación de respuesta
    """
    
    # Validación 1: Verificar que la pregunta no esté vacía
    if not data.question.strip():
        # Registrar advertencia en el log
        logger.warning("ASK | invalid_input | empty_question")
        # Devolver error 400
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La pregunta no puede estar vacía"
        )
    
    # Validación 2: Verificar lenguaje inapropiado
    if contains_inappropriate_language(data.question):
        # Registrar que se bloqueó por contenido inapropiado
        logger.info("ASK | blocked | reason=inappropriate_language")
        # Devolver respuesta de rechazo (NO lanzar excepción)
        # Esto es una respuesta válida, no un error
        return {
            "question": data.question,
            "answer": "No puedo responder a este tipo de consultas.",
            "grounded": False,           # No está basada en documentos
            "context_used": None,        # No hay contexto
            "similarity_score": None     # No hay score
        }
    
    # Registrar que inició el procesamiento
    logger.info("ASK | start | question_len=%s", len(data.question))

    # Intentar generar la respuesta
    try:
        # Llamar a answer_question que hace:
        # 1. Búsqueda semántica
        # 2. Construcción de prompt
        # 3. Llamada al LLM
        result = answer_question(data.question)
    except Exception:
        # Si algo falla, registrar el error
        logger.error("ASK | external_failure")
        # Devolver error 500
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="El servicio externo no pudo procesar la solicitud en este momento"
        )
    
    # Registrar el éxito con detalles
    # result.get() devuelve None si la clave no existe
    logger.info(
        "ASK | success | grounded=%s | similarity=%s",
        result.get("grounded"),
        result.get("similarity_score")
    )

    # Devolver la respuesta completa
    return {
        "question": data.question,                   # Pregunta original
        "answer": result["answer"],                  # Respuesta generada
        "grounded": result["grounded"],              # Si está basada en docs
        "context_used": result.get("context_used"),  # Contexto usado (puede ser None)
        "similarity_score": result.get("similarity_score")  # Score (puede ser None)
    }