# ========================================
# ARCHIVO PRINCIPAL - main.py
# ========================================
# Este es el punto de entrada de toda la aplicación.
# Configura FastAPI y conecta todas las rutas (endpoints)
# ========================================

# Importar FastAPI (el framework web para crear APIs)
from fastapi import FastAPI, Request, HTTPException
# Importar JSONResponse para devolver respuestas en formato JSON
from fastapi.responses import JSONResponse
# Importar load_dotenv para cargar variables de entorno desde .env
from dotenv import load_dotenv

# Importar todos los routers (cada uno maneja diferentes endpoints)
from routers.upload_router import router as upload_router
from routers.embedding_router import router as embedding_router
from routers.search_router import router as search_router
from routers.ask_router import router as ask_router

# Cargar variables de entorno del archivo .env (API keys, etc.)
load_dotenv()

# Crear la aplicación FastAPI con título y versión
app = FastAPI(title="Get Talent: Challenge 4", version="1.0.0")

# Conectar cada router a la aplicación
# Esto hace que los endpoints de cada router estén disponibles
app.include_router(upload_router)      # POST /upload
app.include_router(embedding_router)   # POST /generate-embeddings
app.include_router(search_router)      # POST /search
app.include_router(ask_router)         # POST /ask

# Manejador global de excepciones HTTP
# Se ejecuta cada vez que se lanza una HTTPException
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Maneja todas las excepciones HTTP de la aplicación.
    Si el error es 500, devuelve formato {"error": mensaje}
    Para otros errores, devuelve formato {"detail": mensaje}
    """
    # Verificar si es un error 500 (Internal Server Error)
    if exc.status_code == 500:
        # Devolver con formato especial para errores 500
        return JSONResponse(status_code=500, content={"error": exc.detail})
    # Para cualquier otro error (400, 404, etc.)
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
