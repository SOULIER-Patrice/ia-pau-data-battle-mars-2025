import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline 

from langchain_huggingface import HuggingFaceEmbeddings

from langchain_community.vectorstores import FAISS
import os








def load_knowledge_vector_database(embedding_path, model_name_rag_embedding, device="cpu"):
    embedding_model = HuggingFaceEmbeddings(
    model_name=model_name_rag_embedding,
    multi_process=True,
    model_kwargs={"device": device},  # replace 'cpu' by 'cuda' if you have Nvidia gpu
    encode_kwargs={"normalize_embeddings": True},  # Set `True` for cosine similarity
    )

    knowledge_vector_database = FAISS.load_local(embedding_path, embedding_model, allow_dangerous_deserialization=True)
    return knowledge_vector_database

def load_reader_llm(reader_model, reader_tokenizer):
    reader_llm = pipeline(
    model=reader_model,
    tokenizer=reader_tokenizer,
    task="text-generation",
    do_sample=True,
    temperature=0.2,
    repetition_penalty=1.1,
    return_full_text=False,
    max_new_tokens=500,
    )
    return reader_llm


def get_prompt_template(reader_tokenizer):
    prompt_in_chat_format = [
    {
        "role": "system",
        "content": """Use the information contained in the context to provide a comprehensive answer to the question.  
        - Answer only the question asked, in a concise and relevant manner.  
        - Always cite the sources used by indicating their.  
        - Explain why each reference was used to support the answer.  
        - If the answer cannot be deduced from the context, do not provide one.
        
        Exemple:
        - The correct answer is ...
        - Reference sources used: explain each reference and why you use them.
        - If the question was a multiple choice, explain why the other choise are wrong.
        """,
    },
    {
        "role": "user",
        "content": """Context:
    {context}
    ---
    Now here is the question you need to answer.

    Question: {question}""",
        },
    ]
    return reader_tokenizer.apply_chat_template(
        prompt_in_chat_format, tokenize=False, add_generation_prompt=True
    )

def get_answer(question_query, device="cpu"):
    READER_MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"
    reader_model = AutoModelForCausalLM.from_pretrained(READER_MODEL_NAME)
    reader_tokenizer = AutoTokenizer.from_pretrained(READER_MODEL_NAME)  

    reader_llm = load_reader_llm(reader_model, reader_tokenizer)

    MODEL_NAME_RAG_EMBEDDING = "thenlper/gte-small"
    embedding_path = os.path.abspath('./embeddings/rag_embeddings_gte-small')

    knowledge_vector_database = load_knowledge_vector_database(embedding_path, MODEL_NAME_RAG_EMBEDDING, device)  
    
    retrieved_docs = knowledge_vector_database.similarity_search(query=question_query, k=5)


    context = "\nExtracted documents:\n"

    context += "".join([f'Content: {doc.page_content} \nSource: {doc.metadata['ref']}\n\n' for i, doc in enumerate(retrieved_docs)])

    rag_prompt_tamplate = get_prompt_template(reader_tokenizer)

    final_prompt = rag_prompt_tamplate.format(question=question_query, context=context)

    # Redact an answer
    answer = reader_llm(final_prompt)[0]["generated_text"]
    return answer


if __name__ == "__main__":
    question_query = """Your Client, A Inc, is a sub-licensee under European patent application EP-1. Can the sub-licence be recorded in the European Patent Register?
 
    A    No, it is not possible to record sub-licences in the European Patent Register.
    
    B    Yes, any sub-licence can be recorded in the European Patent Register.
    
    C    Yes, provided the licensee granting the sub-licence has recorded its licence in the European Patent Register.
    """
    answer = get_answer(question_query)
    print(answer)