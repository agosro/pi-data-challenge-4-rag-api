# Se encarga de dividir textos largos en fragmentos más pequeños (chunks). Utiliza RecursiveCharacterTextSplitter de LangChain con un tamaño de chunk de 500 caracteres y una superposición (overlap) de 50 caracteres para mantener el contexto entre cortes.
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Creamos el splitter
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