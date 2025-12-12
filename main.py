# Es el punto de entrada de la aplicación. Configura la instancia de FastAPI, carga las variables de entorno y conecta (incluye) todos los "routers" (las rutas de la API) definidos en la carpeta routers/. También define un manejador de excepciones global para asegurar que los errores 500 se devuelvan con el formato JSON correcto.
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

from routers.upload_router import router as upload_router
from routers.embedding_router import router as embedding_router
from routers.search_router import router as search_router
from routers.ask_router import router as ask_router

load_dotenv()

app = FastAPI(title="Get Talent: Challenge 4", version="1.0.0")

app.include_router(upload_router) # Ruta para subir documentos
app.include_router(embedding_router) # Ruta para generar embeddings
app.include_router(search_router) # Ruta para búsqueda semántica
app.include_router(ask_router) # Ruta para hacer preguntas al LLM

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    # Si es 500, devolvemos el formato exigido por el enunciado
    if exc.status_code == 500:
        return JSONResponse(status_code=500, content={"error": exc.detail})
    # Para el resto, dejamos el estándar
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
