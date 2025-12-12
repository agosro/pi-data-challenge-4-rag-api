# Es el cliente que conecta con la API de Cohere. Tiene dos funciones: embed_documents (para vectorizar los chunks de texto) y embed_query (para vectorizar la pregunta del usuario).
from dotenv import load_dotenv
import cohere
import os

load_dotenv()

co = cohere.ClientV2(api_key=os.getenv("CO_API_KEY"))

def embed_documents(texts: list[str]):
    """
    Embeddings para documentos / chunks.
    """
    response = co.embed(
        texts=texts,
        model="embed-multilingual-v3.0",
        input_type="search_document",
        embedding_types=["float"]
    )
    return response.embeddings.float


def embed_query(text: str):
    """
    Embedding para una consulta del usuario.
    """
    response = co.embed(
        texts=[text],
        model="embed-multilingual-v3.0",
        input_type="search_query",
        embedding_types=["float"]
    )
    return response.embeddings.float[0]