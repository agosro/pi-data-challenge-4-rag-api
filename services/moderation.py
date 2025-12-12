INAPPROPRIATE_KEYWORDS = [
    "idiota",
    "estúpido",
    "imbécil",
    "odio",
    "matar",
    "violencia",
    "racista",
    "sexista"
]

def contains_inappropriate_language(text: str) -> bool:
    text_lower = text.lower()
    return any(word in text_lower for word in INAPPROPRIATE_KEYWORDS)
