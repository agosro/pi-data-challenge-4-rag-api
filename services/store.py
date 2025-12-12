# ========================================
# ALMACENAMIENTO - services/store.py
# ========================================
# Base de datos simple que guarda documentos originales
# Los guarda en un archivo JSON para que persistan
# ========================================

# Importar uuid para generar IDs únicos
import uuid
# Importar json para leer/escribir archivos JSON
import json
# Importar os para verificar si archivos existen
import os

# Ruta del archivo donde se guardan los documentos
DOCUMENTS_FILE = "./documents.json"

# Diccionario en memoria que actúa como base de datos
# Estructura: {"id-del-documento": {"id": ..., "title": ..., "content": ...}}
DOCUMENT_DB = {}

# Función para cargar documentos desde el archivo al iniciar
def load_documents():
    """
    Lee el archivo documents.json y carga los documentos en memoria.
    Se ejecuta automáticamente cuando se importa este módulo.
    """
    global DOCUMENT_DB  # Necesario para modificar la variable global
    # Verificar si el archivo existe
    if os.path.exists(DOCUMENTS_FILE):
        # Abrir el archivo en modo lectura
        with open(DOCUMENTS_FILE, 'r') as f:
            # Cargar el contenido JSON al diccionario
            DOCUMENT_DB = json.load(f)

# Función para guardar documentos al disco
def save_to_disk():
    """
    Escribe el diccionario DOCUMENT_DB en el archivo documents.json.
    Se llama cada vez que se guarda un nuevo documento.
    """
    # Abrir el archivo en modo escritura (sobrescribe el contenido)
    with open(DOCUMENTS_FILE, 'w') as f:
        # Convertir el diccionario a JSON y guardarlo
        json.dump(DOCUMENT_DB, f)

# Cargar documentos al iniciar el módulo
load_documents()

def save_document(title: str, content: str) -> str:
    """
    Guarda un nuevo documento en la base de datos.
    
    Args:
        title: Título del documento
        content: Contenido completo del documento
    
    Returns:
        El ID único generado para el documento (UUID)
    """
    # Generar un ID único usando UUID4
    doc_id = str(uuid.uuid4())

    # Crear el documento como un diccionario
    DOCUMENT_DB[doc_id] = {
        "id": doc_id,
        "title": title,
        "content": content
    }
    
    # Guardar inmediatamente en disco para persistencia
    save_to_disk()
    
    # Devolver el ID para que el cliente lo conozca
    return doc_id


def get_document(document_id: str):
    """
    Recupera un documento por su ID.
    
    Args:
        document_id: El UUID del documento a buscar
    
    Returns:
        El diccionario del documento o None si no existe
    """
    # .get() devuelve None si la clave no existe (seguro)
    return DOCUMENT_DB.get(document_id)

def get_all_documents():
    """
    Devuelve todos los documentos almacenados.
    
    Returns:
        Una vista de los valores del diccionario (todos los documentos)
    """
    # .values() devuelve solo los valores, no las claves
    return DOCUMENT_DB.values()