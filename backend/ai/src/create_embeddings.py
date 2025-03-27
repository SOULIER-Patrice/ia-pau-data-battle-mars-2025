import torch
from transformers import AutoTokenizer, AutoModel

from langchain.docstore.document import Document as LangchainDocument
from langchain.text_splitter import RecursiveCharacterTextSplitter


from langchain_huggingface import HuggingFaceEmbeddings

from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores.utils import DistanceStrategy

import pandas as pd
import numpy as np 
from tqdm import tqdm
from typing import List
import json
import glob


def create_classification_embeddings(model_name, categories_path, output_dir):
    tokenizer_classification = AutoTokenizer.from_pretrained(model_name)
    model_classification = AutoModel.from_pretrained(model_name)

    embeddings_dict = {}
    # Charger le JSON avec un encodage spécifique
    with open(categories_path, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)

    # Extraire les embeddings pour chaque catégorie
    for category, subcategories in data.items():
        for subcategory, details in subcategories.items():
            text = f"{category} {subcategory} {details['Scope']} {details['sentences']}"

            inputs = tokenizer_classification(text, return_tensors="pt", padding=True, truncation=True)
            with torch.no_grad():
                outputs = model_classification(**inputs)
    
            last_hidden_state = outputs.last_hidden_state  # (batch_size, seq_len, hidden_dim)
            attention_mask = inputs["attention_mask"].unsqueeze(-1)
            embeddings = (last_hidden_state * attention_mask).sum(dim=1) / attention_mask.sum(dim=1)
            embeddings_dict[f"{category}_{subcategory}"] = embeddings.numpy()
    
    # Sauvegarder les embeddings dans un fichier .npy
    np.save(f"{output_dir}/categories_{model_name.split("/")[-1]}.npy", embeddings_dict)


def load_csv(data_dir):
    # Load all CSV
    csv_files = glob.glob(f"{data_dir}/*.csv")
    df_list = [pd.read_csv(file) for file in csv_files]
    df = pd.concat(df_list, ignore_index=True) if df_list else pd.DataFrame(columns=["ref", "url", "content"])

    # List of documents for LangChain
    return  [
        LangchainDocument(page_content=row["content"], metadata={"ref": row["ref"], "url": row["url"]})
        for _, row in tqdm(df.iterrows(), total=len(df))
    ]


def load_exam_solutions(data_dir):
    # Load JSON with "solution" in their name
    json_files = glob.glob(f"{data_dir}/*solution*.json")

    json_documents = []
    for file in json_files:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # Extract justification and create Langchain documents
        filename = os.path.basename(file)  # Nom du fichier sans le chemin

        # Si le fichier contient "open" dans son nom, on récupère tout
        if "open" in filename:
            for key, entry in data.items():
                json_documents.append(
                    LangchainDocument(
                        page_content=entry,
                        metadata={"ref": filename}
                    )
                )
            
        else:
            for key, entry in data.items():
                if "Justification" in entry:
                    json_documents.append(
                        LangchainDocument(
                            page_content=entry["Justification"],
                            metadata={"ref": filename}  # ref = Nom du fichier
                        )
                    )
    return json_documents


def split_documents(chunk_size: int, knowledge_base: List[LangchainDocument], tokenizer_name: str, markdown_separators) -> List[LangchainDocument]:
    """
    Split documents into chunks of maximum size `chunk_size` tokens and return a list of documents.
    """
    text_splitter = RecursiveCharacterTextSplitter.from_huggingface_tokenizer(
        AutoTokenizer.from_pretrained(tokenizer_name),
        chunk_size=chunk_size,
        chunk_overlap=int(chunk_size / 10),
        add_start_index=True,
        strip_whitespace=True,
        separators=markdown_separators,
    )

    docs_processed = []
    for doc in knowledge_base:
        docs_processed += text_splitter.split_documents([doc])

    # Remove duplicates
    unique_texts = {}
    docs_processed_unique = []
    for doc in docs_processed:
        if doc.page_content not in unique_texts:
            unique_texts[doc.page_content] = True
            docs_processed_unique.append(doc)

    return docs_processed_unique


def create_rag_embeddings(model_name, markdown_separators, data_dir, output_dir, device="cpu"):
    
    csv_raw_knowledge = load_csv(data_dir)
    exam_raw_knowledge = load_exam_solutions(data_dir)
    raw_knowledge_base = csv_raw_knowledge + exam_raw_knowledge
    
    docs_processed = split_documents(
    512,  # We choose a chunk size adapted to our model
    raw_knowledge_base,
    model_name,
    markdown_separators
    )

    embedding_model = HuggingFaceEmbeddings(
    model_name=model_name,
    multi_process=True,
    model_kwargs={"device": device},  # replace 'cpu' by 'cuda' if you have Nvidia gpu
    encode_kwargs={"normalize_embeddings": True},  # Set `True` for cosine similarity
    )

    # Compute embeddings (can take time ~7min on my laptop)
    knowledge_vector_database = FAISS.from_documents(
        docs_processed, embedding_model, distance_strategy=DistanceStrategy.COSINE
    )
    # Save embeddings
    knowledge_vector_database.save_local(f"{output_dir}/rag_embeddings_{model_name.replace('/', '_')}")



if __name__ == "__main__":
    import os
    from config.config import model_classification, model_rag

    categories_path = os.path.abspath('ai/outputs/categories.json')
    output_dir = os.path.abspath('ai/embeddings')
    print(categories_path)
    print(output_dir)
    
    create_classification_embeddings(model_classification, categories_path, output_dir)


    markdown_separators = [
    "\n\n",
    "\n",
    ".",
    " ",
    "",
    ]
    

    data_dir = os.path.abspath('ai/outputs')
    output_dir = os.path.abspath('ai/embeddings')
    print(categories_path)
    print(output_dir)

    create_rag_embeddings(model_rag, markdown_separators, data_dir, output_dir, device="cuda")