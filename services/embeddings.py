# ========================================
# EMBEDDINGS - services/embeddings.py
# ========================================
# Genera vectores (embeddings) usando la API de Cohere
# Los vectores son representaciones numéricas del significado del texto
# ========================================

# Importar load_dotenv para cargar variables de entorno
from dotenv import load_dotenv
# Importar el cliente de Cohere
import cohere
# Importar os para leer variables de entorno
import os

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Crear cliente de Cohere con la API key del archivo .env
# La API key se obtiene de la variable CO_API_KEY
co = cohere.ClientV2(api_key=os.getenv("CO_API_KEY"))

# Función para generar embeddings de documentos
def embed_documents(texts: list[str]):
    """
    Convierte una lista de textos (chunks) en vectores.
    Se usa para documentos que queremos guardar en la base de datos.
    
    Args:
        texts: Lista de strings (chunks de documentos)
    
    Returns:
        Lista de vectores (cada uno es una lista de números float)
    
    Ejemplo:
        chunks = ["Python es genial", "Me gusta programar"]
        vectores = embed_documents(chunks)
        # Resultado: [[0.1, 0.5, ...], [0.3, 0.2, ...]]
    """
    # Llamar a la API de Cohere
    response = co.embed(
        texts=texts,                              # Los textos a vectorizar
        model="embed-multilingual-v3.0",          # Modelo multilingüe (español, inglés, etc.)
        input_type="search_document",             # Tipo: documento (no consulta)
        embedding_types=["float"]                 # Formato: números decimales
    )
    # Devolver solo los vectores en formato float
    return response.embeddings.float


# Función para generar embedding de una consulta
def embed_query(text: str):
    """
    Convierte una consulta del usuario en un vector.
    Se usa para la pregunta/búsqueda que hace el usuario.
    
    Args:
        text: String con la consulta del usuario
    
    Returns:
        Un vector (lista de números float)
    
    Ejemplo:
        pregunta = "¿Qué es Python?"
        vector = embed_query(pregunta)
        # Resultado: [0.2, 0.7, 0.1, ...]
    """
    # Llamar a la API de Cohere
    response = co.embed(
        texts=[text],                             # Enviar como lista de un elemento
        model="embed-multilingual-v3.0",          # Mismo modelo que para documentos
        input_type="search_query",                # Tipo: consulta (optimizado para búsqueda)
        embedding_types=["float"]                 # Formato: números decimales
    )
    # Devolver solo el primer vector (ya que solo enviamos un texto)
    return response.embeddings.float[0]