# Funciona como una base de datos simple en memoria (un diccionario de Python) para guardar los documentos originales (título y contenido) antes de procesarlos, asignándoles un ID único.
import uuid

# Base de datos en memoria
DOCUMENT_DB = {}


def save_document(title: str, content: str) -> str:
    """
    Guarda un documento y devuelve su ID.
    """
    doc_id = str(uuid.uuid4())

    DOCUMENT_DB[doc_id] = {
        "id": doc_id,
        "title": title,
        "content": content
    }

    return doc_id


def get_document(document_id: str):
    """
    Recupera un documento por ID.
    """
    # print("DOCUMENTS:", DOCUMENT_DB.keys())
    return DOCUMENT_DB.get(document_id)

def get_all_documents():
    return DOCUMENT_DB.values()