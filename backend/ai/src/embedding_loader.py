from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import config.ai as ai

# Embedding model
def load_rag_embeddings(path=f'./ai/embeddings/rag_embeddings_{ai.model_rag.replace('/', '_')}'):

    embedding_model = HuggingFaceEmbeddings(
        model_name=ai.model_rag,
        multi_process=True,
        model_kwargs={"device": "cpu"},  # replace 'cpu' by 'cuda' if you have Nvidia gpu
        encode_kwargs={"normalize_embeddings": True},  # Set `True` for cosine similarity
    )
    
    knowledge_vector_db = FAISS.load_local(path, embedding_model, allow_dangerous_deserialization=True)
    print("embedding load")
    return knowledge_vector_db