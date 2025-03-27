# Imports
import json
import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

import ollama
from ollama import chat
import re
from fastapi import FastAPI

# --------------------------------------------------------
# ENV variables and loading models in memory
# --------------------------------------------------------

# To prelo!ad a model and leave it in memory (for faster inference)
# !curl -X POST http://localhost:11434/api/generate -H "Content-Type: application/json" -d "{\"model\": \"qwen2.5:7b\", \"keep_alive\": -1}"
# To unload a model and free up memory
# !curl -X POST http://localhost:11434/api/generate -H "Content-Type: application/json" -d "{\"model\": \"qwen2.5:7b\", \"keep_alive\": 0}"

# Embedding model
def load_rag_embeddings(path="./ai/embeddings/rag_embeddings_gte-small"):
    EMBEDDING_MODEL_NAME = "thenlper/gte-small"

    embedding_model = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME,
        multi_process=True,
        model_kwargs={"device": "cpu"},  # replace 'cpu' by 'cuda' if you have Nvidia gpu
        encode_kwargs={"normalize_embeddings": True},  # Set `True` for cosine similarity
    )
    KNOWLEDGE_VECTOR_DATABASE = FAISS.load_local(path, embedding_model, allow_dangerous_deserialization=True)
    return KNOWLEDGE_VECTOR_DATABASE


# Reader model
MODEL = 'qwen2.5:7b'
MAX_OUTPUT_TOKENS = 3000

# --------------------------------------------------------
# Functions used in other RAG functions 
# --------------------------------------------------------

def get_context(query, k=5, KNOWLEDGE_VECTOR_DATABASE=None):
    from main import app 
    """ Récupère le contexte pertinent pour une requête. """
    if KNOWLEDGE_VECTOR_DATABASE is None:
        KNOWLEDGE_VECTOR_DATABASE = getattr(app.state, "knowledge_vector_db", None)    
        
    if KNOWLEDGE_VECTOR_DATABASE is None:
        raise ValueError("KNOWLEDGE_VECTOR_DATABASE n'est pas initialisé")
    
    
    retrieved_docs = KNOWLEDGE_VECTOR_DATABASE.similarity_search(query=query, k=k)
    return retrieved_docs


def validate_json_format_mcq(llm_output, type):
    """
    Attempts to extract and validate a JSON structure from the LLM output.

    Parameters:
    llm_output (str): Raw output from the LLM.
    type (str): question or answer

    Returns:
    dict: A valid JSON object if found and correctly formatted, otherwise None.
    """

    if type == 'question':
        try:
            json_match = re.search(r'\{.*\}', llm_output, re.DOTALL)
            if json_match:
                cleaned_json = json.loads(json_match.group())
                if "question" in cleaned_json and "options" in cleaned_json:
                    return cleaned_json
        except json.JSONDecodeError:
            pass
        return None
    
    elif type == 'answer':
        try:
            json_match = re.search(r'\{.*\}', llm_output, re.DOTALL)
            if json_match:
                cleaned_json = json.loads(json_match.group())
                if "Answer" in cleaned_json and "Justification" in cleaned_json:
                    answer = cleaned_json["Answer"]
                    # Check if answer in 'A', 'B', 'C', or 'D'.
                    if answer not in {'A', 'B', 'C', 'D'}:
                        # check for a valid letter isolated
                        match = re.search(r'\b[A-D]\b', answer)
                        if match:
                            cleaned_json["Answer"] = match.group()
                        else:
                            return None
                    return cleaned_json
        except json.JSONDecodeError:
            pass
        return None


def call_formatting_llm_mcq(llm_output, type):
    """
    Calls an LLM specialized in formatting text into the correct JSON format.

    Parameters:
    llm_output (str): Raw output from the initial LLM.
    type (str): question or answer

    Returns:
    dict: A valid JSON object containing the question and options.
    """

    if type == 'question':
        SYSTEM_PROMPT = """You are an AI specialized in converting multiple-choice legal questions into JSON format.
        Ensure the output strictly follows this structure:
        ```json
        {"question": "...", "options": ["A ....", "B ...", "C ...", "D ..."]}
        """

    elif type == 'answer':
        SYSTEM_PROMPT = """You are an AI specialized in converting legal answer into JSON format.
        Ensure the output strictly follows this structure:
        ```json
        {
        "Answer": "...", 
        "Justification": "..."
        }
        """

    user_prompt = f"""
        The following text needs to be formatted as a valid JSON:
        {llm_output}
        
        Please convert it into the required JSON format.
        """

    response = chat(model=MODEL, messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ])
    
    return validate_json_format_mcq(response['message']['content'], type)


def clean_generate_mcq_output(llm_output, type):
    """
    Cleans and extracts a valid JSON multiple-choice question from the LLM output.
    If the initial output is not valid JSON, a specialized LLM is called to correct it.

    Parameters:
    llm_output (str): Raw output from the LLM.

    Returns:
    dict: A properly formatted multiple-choice question.
    """
    result = validate_json_format_mcq(llm_output, type)
    if result:
        return result
    
    # If not valid, call formatting LLM
    formatted_result = call_formatting_llm_mcq(llm_output, type)
    if formatted_result:
        return formatted_result
    
    raise ValueError("Failed to convert LLM output into valid JSON format.")