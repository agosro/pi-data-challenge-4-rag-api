from langchain_text_splitters import RecursiveCharacterTextSplitter

# Creamos el splitter una sola vez
_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,      # tamaño del chunk en caracteres
    chunk_overlap=50,    # solapamiento para no cortar ideas
    separators=["\n\n", "\n", ".", " "]  # prioridad de corte
)

def chunk_text(text: str) -> list[str]:
    """
    Divide un texto largo en chunks semánticamente coherentes.
    """
    return _splitter.split_text(text)