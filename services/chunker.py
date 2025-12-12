# ========================================
# CHUNKER - services/chunker.py
# ========================================
# Divide textos largos en fragmentos pequeños (chunks)
# Esto es necesario porque los embeddings funcionan mejor con textos cortos
# ========================================

# Importar el divisor de texto de LangChain
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Crear un objeto splitter (divisor) con configuración específica
# Se crea una sola vez y se reutiliza para todos los textos
_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,      # Cada chunk tendrá máximo 500 caracteres
    chunk_overlap=50,    # Los chunks se solapan 50 caracteres para no perder contexto
    separators=["\n\n", "\n", ".", " "]  # Prioridad de dónde cortar:
                         # 1º: doble salto de línea (párrafos)
                         # 2º: salto de línea simple
                         # 3º: punto (fin de oración)
                         # 4º: espacio (entre palabras)
)

def chunk_text(text: str) -> list[str]:
    """
    Divide un texto largo en una lista de fragmentos (chunks).
    
    Args:
        text: El texto completo a dividir
    
    Returns:
        Una lista de strings, cada uno con máximo 500 caracteres
    
    Ejemplo:
        texto = "Este es un texto muy largo..."
        chunks = chunk_text(texto)
        # Resultado: ["Este es un texto...", "...muy largo..."]
    """
    # Llamar al método split_text del objeto _splitter
    return _splitter.split_text(text)