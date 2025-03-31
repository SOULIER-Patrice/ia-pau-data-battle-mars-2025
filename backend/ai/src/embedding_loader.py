from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os

# Embedding model


def load_rag_embeddings(model_name, device='cuda'):

    output_dir = os.path.abspath('ai/embeddings')
    path = f"{output_dir}/rag_embeddings_{model_name.replace('/', '_')}"

    if device == 'cpu':
        embedding_model = HuggingFaceEmbeddings(
            model_name=model_name,
            multi_process=True,
            # replace 'cpu' by 'cuda' if you have Nvidia gpu
            model_kwargs={"device": "cpu", "trust_remote_code": True},
            # Set `True` for cosine similarity
            encode_kwargs={"normalize_embeddings": True},
        )
    else:
        embedding_model = HuggingFaceEmbeddings(
            model_name=model_name,
            multi_process=True,
            # replace 'cpu' by 'cuda' if you have Nvidia gpu
            model_kwargs={"device": "cuda", "trust_remote_code": True},
            # Set `True` for cosine similarity
            encode_kwargs={"normalize_embeddings": True},
        )

    knowledge_vector_db = FAISS.load_local(
        path, embedding_model, allow_dangerous_deserialization=True)
    return knowledge_vector_db
