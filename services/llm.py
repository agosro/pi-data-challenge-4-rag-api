# Contiene la lógica para "Responder preguntas" (RAG). Busca el contexto más relevante, construye un prompt con reglas de "Grounding" (para que no invente datos) y envía todo al modelo command-r-plus-08-2024 de Cohere para generar la respuesta final.
from dotenv import load_dotenv
import cohere
import os
from services.search import semantic_search

load_dotenv()

co = cohere.ClientV2(os.getenv("COHERE_API_KEY"))

MIN_SIMILARITY = 0.50

def build_prompt(contexto: str, pregunta: str) -> str:
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

# Responder pregunta con grounding
def answer_question(question: str):
    results = semantic_search(question, top_k=1)

    # Grounding obligatorio: sin contexto suficiente
    if not results or results[0]["similarity_score"] < MIN_SIMILARITY:
        return {
            "answer": "No cuento con información suficiente para responder a esta consulta.",
            "grounded": False,
            "context_used": None,
            "similarity_score": None
        }

    top = results[0]

    prompt = build_prompt(
        contexto=top["content_snippet"],
        pregunta=question
    )

    response = co.chat(
        model="command-r-plus-08-2024",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    answer_text = response.message.content[0].text.strip()

    if not answer_text:
        return {
        "answer": "No cuento con información suficiente para responder a esta consulta.",
        "grounded": False,
        "context_used": top["content_snippet"],
        "similarity_score": top["similarity_score"]
    }


    return {
        "answer": answer_text,
        "grounded": True,
        "context_used": top["content_snippet"],
        "similarity_score": top["similarity_score"]
    }
