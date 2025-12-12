# ========================================
# MODERATION - services/moderation.py
# ========================================
# Filtro de contenido inapropiado
# Detecta palabras ofensivas o peligrosas en el texto
# ========================================

# Lista de palabras prohibidas (keywords bloqueadas)
# Esta es una implementación simple; en producción se usarían APIs especializadas
INAPPROPRIATE_KEYWORDS = [
    "idiota",      # Insulto
    "estúpido",    # Insulto
    "imbécil",     # Insulto
    "odio",        # Lenguaje de odio
    "matar",       # Violencia
    "violencia",   # Violencia
    "racista",     # Discriminación
    "sexista",     # Discriminación
]

def contains_inappropriate_language(text: str) -> bool:
    """
    Verifica si un texto contiene lenguaje inapropiado.
    
    Args:
        text: El texto a verificar (puede ser una pregunta o documento)
    
    Returns:
        True si contiene palabras prohibidas, False si está limpio
    
    Ejemplo:
        contains_inappropriate_language("Hola")        # False
        contains_inappropriate_language("Eres idiota") # True
    """
    # Convertir todo a minúsculas para comparación case-insensitive
    text_lower = text.lower()
    
    # any() devuelve True si ALGUNA palabra prohibida está en el texto
    # Itera sobre cada palabra en INAPPROPRIATE_KEYWORDS
    # Para cada palabra, verifica si está contenida en text_lower
    return any(word in text_lower for word in INAPPROPRIATE_KEYWORDS)
