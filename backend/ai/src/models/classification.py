from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoTokenizer, AutoModel
import torch


def get_embeddings(text, model_name="nlpaueb/bert-base-uncased-eurlex", method="cls"):
    """Extrait l'embedding d'une phrase selon la méthode spécifiée."""
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)

    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    
    with torch.no_grad():
        outputs = model(**inputs)
    
    last_hidden_state = outputs.last_hidden_state  # (batch_size, seq_len, hidden_dim)
    
    if method == "cls":
        return last_hidden_state[:, 0, :]  # Embedding du token [CLS]
    elif method == "mean":
        attention_mask = inputs["attention_mask"].unsqueeze(-1)
        embeddings = (last_hidden_state * attention_mask).sum(dim=1) / attention_mask.sum(dim=1)
        return embeddings  # Moyenne des embeddings des tokens
    else:
        raise ValueError("Méthode non reconnue : choisir 'cls' ou 'mean'.")
    

def get_category_question(question, category_embeddings, method="mean"):
    """Classifie la question et retourne la catégorie la plus similaire."""
    # Extraire l'embedding de la question
    question_embedding = get_embeddings(question, method=method)

    # Comparer la question avec chaque catégorie
    best_category = None
    max_similarity = -1  # Initialisation à une valeur très basse

    for category, category_embedding in category_embeddings.items():
        similarity = cosine_similarity(question_embedding.numpy().reshape(1, -1), category_embedding.reshape(1, -1))[0][0]
        if similarity > max_similarity:
            max_similarity = similarity
            best_category = category

    return best_category.split("_")[-1]