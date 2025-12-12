# 📚 Challenge RAG API – FastAPI + Cohere + ChromaDB

Este proyecto implementa una **API de Recuperación Aumentada por Generación (RAG)** utilizando **FastAPI**, **Cohere** y **ChromaDB**, como parte del Challenge Técnico (Semana 4).

La API permite:
- Cargar documentos
- Generar embeddings
- Realizar búsquedas semánticas
- Responder preguntas basadas exclusivamente en el contenido cargado

Todo el sistema incorpora **buenas prácticas de IA Responsable**, como grounding obligatorio, manejo de errores controlado y bloqueo de lenguaje inapropiado.

---

## 🧠 Arquitectura General

**Flujo principal:**

1. **Upload** → Se almacena el documento
2. **Generate Embeddings** → El documento se fragmenta y se vectoriza
3. **Search** → Se recuperan fragmentos relevantes usando similitud semántica
4. **Ask** → El LLM responde solo con el contexto recuperado (RAG)

---

## 🛠️ Tecnologías Utilizadas

- **FastAPI** – Framework para la API
- **Uvicorn** – Servidor ASGI
- **Cohere API** – Generación de embeddings y respuestas con LLM
- **ChromaDB** – Vector store local persistente
- **LangChain** – Chunking de texto (RecursiveCharacterTextSplitter)
- **python-dotenv** – Manejo de variables de entorno

---

## 📦 Instalación

### 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/challenge-rag-fastapi-cohere.git
cd challenge-rag-fastapi-cohere
````

### 2️⃣ Crear entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4️⃣ Configurar variables de entorno

Crear un archivo `.env` en la raíz del proyecto:

```env
CO_API_KEY=tu_api_key_aqui
```

---

## ▶️ Ejecutar la API

```bash
uvicorn main:app --reload
```

La documentación interactiva estará disponible en:

* 👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) (Swagger)
* 👉 [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🔌 Endpoints Principales

### 📥 POST `/upload`

Carga un nuevo documento en el sistema.

### 🧩 POST `/generate-embeddings`

Genera embeddings para un documento previamente cargado.

### 🔍 POST `/search`

Realiza una búsqueda semántica sobre los documentos almacenados.

### ❓ POST `/ask`

Responde una pregunta utilizando únicamente el contexto recuperado desde `/search`.

Incluye:

* `grounded`: indica si la respuesta se basó en contexto real
* `context_used`: fragmento utilizado
* `similarity_score`: similitud del fragmento más relevante

---

## 🛡️ Principios de IA Responsable

✔ **Grounding obligatorio**
✔ **No se inventa información**
✔ **Bloqueo de lenguaje inapropiado**
✔ **No exposición de datos sensibles**
✔ **Mensajes de error genéricos**
✔ **Logs sin contenido sensible**

Si no hay información suficiente, la API responde:

```
"No cuento con información suficiente para responder a esta consulta."
```

---

## 📁 Estructura del Proyecto

```text
.
├── main.py
├── routers/
│   ├── upload_router.py
│   ├── embedding_router.py
│   ├── search_router.py
│   └── ask_router.py
├── services/
│   ├── store.py
│   ├── embeddings.py
    ├── chunker.py
│   ├── vectorstore.py
│   ├── search.py
│   ├── llm.py
│   ├── moderation.py
│   └── logging.py
├── models/
│   └── schemas.py            
├── requirements.txt
└── .env
```

---

## 👤 Autora

**Agostina Rocío Torres**
Analista de Sistemas

---

## 📌 Notas Finales

Este proyecto fue desarrollado con foco en:

* claridad arquitectónica
* separación de responsabilidades
* prácticas responsables de uso de modelos de lenguaje

```

---
