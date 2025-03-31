import torch
from transformers import AutoTokenizer, AutoModel

from langchain.docstore.document import Document as LangchainDocument
from langchain.text_splitter import RecursiveCharacterTextSplitter


from langchain_huggingface import HuggingFaceEmbeddings

from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores.utils import DistanceStrategy

from ai.src.models.classification import get_embeddings, get_categories_question

import pandas as pd
import numpy as np
from tqdm import tqdm
from typing import List
import json
import glob
import os


def add_classification_question(model_name, category_embeddings, data_dir):
    # Récupération des fichiers MCQ et solutions

    mcq_files = sorted([f for f in os.listdir(
        f"{data_dir}/qa") if f.endswith("_mcq.json")])

    for mcq_file in mcq_files:
        file_path = os.path.join(data_dir, "qa", mcq_file)

        # Charger le fichier JSON
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Ajouter la catégorie pour chaque question
        for key, item in data.items():  # Parcourir les paires clé-valeur du dictionnaire
            question = item.get("question", "")
            # Convertir la liste en chaîne
            options = " ".join(item.get("options", []))

            input_text = f"{question} {options}"
            categories = get_categories_question(
                input_text, model_name, category_embeddings)

            # Ajouter les catégories au dictionnaire
            item["categories"] = categories

        # Sauvegarder le fichier JSON modifié
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        print(f"Catégories ajoutées à {mcq_file}")

    open_files = sorted([f for f in os.listdir(
        f"{data_dir}/qa") if f.endswith("_open.json")])

    for open_file in open_files:
        file_path = os.path.join(data_dir, "qa", open_file)

        # Charger le fichier JSON
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

            # Ajouter la catégorie pour chaque question
        for key, item in data.items():  # Parcourir les paires clé-valeur du dictionnaire
            input_text = item.get("question", "")

            categories = get_categories_question(
                input_text, model_name, category_embeddings)

            # Ajouter les catégories au dictionnaire
            item["categories"] = categories

        # Sauvegarder le fichier JSON modifié
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        print(f"Catégories ajoutées à {open_file}")


def create_classification_embeddings(model_name, data_dir, output_dir):
    """Crée les embeddings pour les catégories si le fichier n'existe pas."""

    output_file = f"{output_dir}/categories_{model_name.split('/')[-1]}.npy"
    categories_path = f"{data_dir}/categories.json"
    # Vérifier si le fichier existe déjà
    if os.path.exists(output_file):
        print(
            f"Le fichier {output_file} existe déjà. Les embeddings ne seront pas recréés.")
        return  # Sortir de la fonction si le fichier existe

    embeddings_dict = {}
    # Charger le JSON avec un encodage spécifique
    with open(categories_path, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)

    # Extraire les embeddings pour chaque catégorie
    for category, subcategories in data.items():
        for subcategory, details in subcategories.items():
            text = f"{category} {subcategory} {details['Scope']} {details['sentences']}"
            # Ou "cls" selon ce que tu préfères
            embedding = get_embeddings(text, model_name)
            embeddings_dict[f"{category}_{subcategory}"] = embedding.numpy()

    # Sauvegarder les embeddings dans un fichier .npy
    print(f"Création des embeddings et sauvegarde dans : {output_file}")
    np.save(output_file, embeddings_dict)


def load_csv(data_dir):
    # Load all CSV
    csv_files = glob.glob(f"{data_dir}/official_legal_publications/*.csv")
    df_list = [pd.read_csv(file) for file in csv_files]
    df = pd.concat(df_list, ignore_index=True) if df_list else pd.DataFrame(
        columns=["ref", "url", "content"])

    # List of documents for LangChain
    return [
        LangchainDocument(page_content=row["content"], metadata={
                          "ref": row["ref"], "url": row["url"]})
        for _, row in tqdm(df.iterrows(), total=len(df))
    ]


def load_exam_solutions(data_dir):
    # Load JSON with "solution" in their name
    json_files = glob.glob(f"{data_dir}/qa/*solution*.json")

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

    output_file = f"{output_dir}/rag_embeddings_{model_name.replace('/', '_')}"

    # Vérifier si le fichier existe déjà
    if os.path.exists(output_file):
        print(
            f"Le fichier {output_file} existe déjà. Les embeddings ne seront pas recréés.")
        return  # Sortir de la fonction si le fichier existe

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
        # replace 'cpu' by 'cuda' if you have Nvidia gpu
        model_kwargs={"device": device, "trust_remote_code":True},
        # Set `True` for cosine similarity
        encode_kwargs={"normalize_embeddings": True},
    )

    # Compute embeddings (can take time ~7min on my laptop)
    knowledge_vector_database = FAISS.from_documents(
        docs_processed, embedding_model, distance_strategy=DistanceStrategy.COSINE
    )
    # Save embeddings
    knowledge_vector_database.save_local(
        f"{output_dir}/rag_embeddings_{model_name.replace('/', '_')}")