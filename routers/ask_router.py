# Endpoint POST /ask. Es el más complejo; verifica si hay lenguaje inapropiado, registra logs de la actividad y llama a answer_question para obtener la respuesta generada por IA.
from fastapi import APIRouter, HTTPException, status
from models.schemas import AskInput, AskResponse
from services.llm import answer_question
from services.moderation import contains_inappropriate_language
from services.logging import logger

router = APIRouter()

@router.post("/ask", response_model=AskResponse, status_code=status.HTTP_200_OK)

def ask_question(data: AskInput):
    
    # Validación de entrada
    if not data.question.strip():
        logger.warning("ASK | invalid_input | empty_question")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La pregunta no puede estar vacía"
        )
    
    # Bloqueo de lenguaje inapropiado
    if contains_inappropriate_language(data.question):
        logger.info("ASK | blocked | reason=inappropriate_language")
        return {
            "question": data.question,
            "answer": "No puedo responder a este tipo de consultas.",
            "grounded": False,
            "context_used": None,
            "similarity_score": None
        }
    
    logger.info("ASK | start | question_len=%s", len(data.question))

    # Generación controlada
    try:
        result = answer_question(data.question)
    except Exception:
        logger.error("ASK | external_failure")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="El servicio externo no pudo procesar la solicitud en este momento"
        )
    
    logger.info(
        "ASK | success | grounded=%s | similarity=%s",
        result.get("grounded"),
        result.get("similarity_score")
    )

    # Respuesta segura (grounding)
    return {
        "question": data.question,
        "answer": result["answer"],
        "grounded": result["grounded"],
        "context_used": result.get("context_used"),
        "similarity_score": result.get("similarity_score")
    }