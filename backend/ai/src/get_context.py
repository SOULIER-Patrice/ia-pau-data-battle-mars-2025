from langchain_community.vectorstores import FAISS

# --------------------------------------------------------
# Functions used in other RAG functions 
# --------------------------------------------------------

def get_context(query: str, k: int, knowledge_vector_db: FAISS):
    """ Récupère le contexte pertinent pour une requête. """

    retrieved_docs = knowledge_vector_db.similarity_search(query=query, k=k)
    return retrieved_docs
