from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from ai.src.embedding_loader import load_rag_embeddings

from api.resources import auth_resource, user_resource, book_resource
from api.resources.state import app_state  # Import du state depuis un module séparé


@asynccontextmanager
async def lifespan(app: FastAPI):
    """ Gère le chargement et la libération des embeddings """
    print("🚀 Chargement des embeddings RAG...")
    app_state["knowledge_vector_db"] = load_rag_embeddings()  # Chargement unique
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
    }
]

app = FastAPI(
    title="IA Pau Databattle 2025",
    openapi_tags=tags_metadata,
    lifespan=lifespan
)

origins = [
    "http://localhost:5173",
    "http://lawrag.duckdns.org",
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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
