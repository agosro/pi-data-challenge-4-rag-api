
import uuid
import json
import os

DOCUMENTS_FILE = "./documents.json"
DOCUMENT_DB = {}

# Cargar documentos al iniciar
def load_documents():
    global DOCUMENT_DB
    if os.path.exists(DOCUMENTS_FILE):
        with open(DOCUMENTS_FILE, 'r') as f:
            DOCUMENT_DB = json.load(f)

# Guardar documentos al disco
def save_to_disk():
    with open(DOCUMENTS_FILE, 'w') as f:
        json.dump(DOCUMENT_DB, f)

load_documents()
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
    save_to_disk()
    return doc_id


def get_document(document_id: str):
    """
    Recupera un documento por ID.
    """
    # print("DOCUMENTS:", DOCUMENT_DB.keys())
    return DOCUMENT_DB.get(document_id)

def get_all_documents():
    return DOCUMENT_DB.values()