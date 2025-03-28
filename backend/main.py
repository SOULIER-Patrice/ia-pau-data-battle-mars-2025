from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from ai.src.embedding_loader import load_rag_embeddings
from config.config import init_ollama_model

from api.resources import auth_resource, user_resource, book_resource, stream_resource
# Import du state depuis un module séparé
from api.resources.state import app_state


@asynccontextmanager
async def lifespan(app: FastAPI):
    """ Gère le chargement et la libération des embeddings """
    print("🚀 Chargement des embeddings RAG...")
    # Chargement unique
    app_state["knowledge_vector_db"] = load_rag_embeddings()
    yield  # L'application tourne ici
    print("🛑 Libération des ressources...")
    app_state["knowledge_vector_db"] = None  # Nettoyage en mémoire


tags_metadata = [
    {
        "name": "Auth"
    },
    {
        "name": "User"
    },
    {
        "name": "Book"
    },
    {
        "name": "Stream"
    },

]

app = FastAPI(
    title="IA Pau Databattle 2025",
    openapi_tags=tags_metadata,
    lifespan=lifespan
)

origins = [
    "http://localhost:5173",
    "http://lawrag.duckdns.org",
    "http://10.0.0.4:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"]
)

app.include_router(auth_resource.router)
app.include_router(user_resource.router)
app.include_router(book_resource.router)
app.include_router(stream_resource.router)


if __name__ == "__main__":
    import uvicorn
    init_ollama_model()
    uvicorn.run(app, host="0.0.0.0", port=8000)
