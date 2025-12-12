# ========================================
# LLM - services/llm.py
# ========================================
# Lógica de RAG (Retrieval Augmented Generation)
# Responde preguntas usando SOLO información de documentos
# ========================================

# Importar load_dotenv para variables de entorno
from dotenv import load_dotenv
# Importar cliente de Cohere para usar el LLM
import cohere
# Importar os para leer variables de entorno
import os
# Importar la función de búsqueda semántica
from services.search import semantic_search

# Cargar variables de entorno del archivo .env
load_dotenv()

# Crear cliente de Cohere con la API key
co = cohere.ClientV2(os.getenv("COHERE_API_KEY"))

# Umbral mínimo de similitud (0.0 a 1.0)
# Si el mejor resultado tiene score < 0.50, no se responde
MIN_SIMILARITY = 0.50

def build_prompt(contexto: str, pregunta: str) -> str:
    """
    Construye el prompt para el LLM con instrucciones de grounding.
    
    Args:
        contexto: Fragmento del documento relevante
        pregunta: Pregunta del usuario
    
    Returns:
        String con el prompt completo formateado
    """
    # Usar f-string para insertar las variables en el template
    return f"""
ROL:
Sos un asistente de lenguaje diseñado para responder consultas de forma precisa y responsable.

IDENTIDAD:
Respondés únicamente utilizando la información presente en el contexto proporcionado.
No utilizás conocimiento previo ni realizás suposiciones.

REGLAS DE GROUNDING:
1. Usá EXCLUSIVAMENTE el contenido dentro de la sección CONTEXTO.
2. NO inventes información.
3. NO combines información de distintos documentos.
4. Si el contexto no contiene la respuesta, respondé EXACTAMENTE:
"No cuento con información suficiente para responder a esta consulta."

SEGURIDAD Y ÉTICA:
1. No incluyas opiniones, juicios subjetivos, estereotipos ni lenguaje ofensivo.
2. No incluyas información sensible que no esté explícitamente presente en el contexto.
3. Respondé de forma neutral y objetiva.

FORMATO DE RESPUESTA:
- Máximo 3 oraciones.
- Clara y concisa.

CONTEXTO:
{contexto}

PREGUNTA:
{pregunta}

RESPUESTA:
"""

# Función principal para responder preguntas
def answer_question(question: str):
    """
    Responde una pregunta usando RAG con grounding estricto.
    
    Args:
        question: La pregunta del usuario
    
    Returns:
        Diccionario con:
        - answer: La respuesta generada
        - grounded: Si está basada en documentos
        - context_used: El contexto utilizado
        - similarity_score: Score de similitud
    """
    # Paso 1: Buscar el documento más relevante (top_k=1)
    results = semantic_search(question, top_k=1)

    # Paso 2: Verificar si hay resultados suficientemente similares
    # Si no hay resultados O el score es muy bajo, no respondemos
    if not results or results[0]["similarity_score"] < MIN_SIMILARITY:
        return {
            "answer": "No cuento con información suficiente para responder a esta consulta.",
            "grounded": False,           # No está basado en documentos
            "context_used": None,        # No hay contexto
            "similarity_score": None     # No hay score
        }

    # Paso 3: Obtener el mejor resultado
    top = results[0]

    # Paso 4: Construir el prompt con el contexto
    prompt = build_prompt(
        contexto=top["content_snippet"],  # Fragmento del documento
        pregunta=question                 # Pregunta original
    )

    # Paso 5: Llamar al LLM de Cohere
    response = co.chat(
        model="command-r-plus-08-2024",   # Modelo de lenguaje
        messages=[{"role": "user", "content": prompt}],  # Conversación
        temperature=0.2                   # Creatividad baja (más preciso)
    )

    # Paso 6: Extraer el texto de la respuesta
    answer_text = response.message.content[0].text.strip()

    # Paso 7: Verificar si el LLM devolvió algo
    if not answer_text:
        # Si la respuesta está vacía, devolver mensaje por defecto
        return {
            "answer": "No cuento con información suficiente para responder a esta consulta.",
            "grounded": False,
            "context_used": top["content_snippet"],
            "similarity_score": top["similarity_score"]
        }

    # Paso 8: Devolver respuesta exitosa
    return {
        "answer": answer_text,                      # Respuesta del LLM
        "grounded": True,                           # Está basada en documentos
        "context_used": top["content_snippet"],    # Contexto usado
        "similarity_score": top["similarity_score"] # Score de similitud
    }
