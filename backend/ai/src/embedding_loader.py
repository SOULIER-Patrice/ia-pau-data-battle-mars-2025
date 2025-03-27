from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Embedding model
def load_rag_embeddings(path="./ai/embeddings/rag_embeddings_thenlper_gte-small"):
    EMBEDDING_MODEL_NAME = "thenlper/gte-small"

    embedding_model = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME,
        multi_process=True,
        model_kwargs={"device": "cpu"},  # replace 'cpu' by 'cuda' if you have Nvidia gpu
        encode_kwargs={"normalize_embeddings": True},  # Set `True` for cosine similarity
    )
    
    knowledge_vector_db = FAISS.load_local(path, embedding_model, allow_dangerous_deserialization=True)
    print("embedding load")
    return knowledge_vector_db