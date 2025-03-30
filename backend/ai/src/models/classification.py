from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoTokenizer, AutoModel
import torch


def get_embeddings(text, model_name):
    """Extrait l'embedding d'une phrase selon la méthode spécifiée."""
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)

    inputs = tokenizer(text, return_tensors="pt",
                       padding=True, truncation=False)

    with torch.no_grad():
        outputs = model(**inputs)

    # (batch_size, seq_len, hidden_dim)
    last_hidden_state = outputs.last_hidden_state

    attention_mask = inputs["attention_mask"].unsqueeze(-1)
    embeddings = (last_hidden_state *
                  attention_mask).sum(dim=1) / attention_mask.sum(dim=1)

    embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)
    return embeddings  # Moyenne des embeddings des tokens


def get_categories_question(question, model_name, category_embeddings):
    """Classifie la question et retourne les 3 catégories les plus similaires."""
    # Extraire l'embedding de la question
    question_embedding = get_embeddings(question, model_name)

    # Comparer la question avec chaque catégorie
    similarities = {}
    for category, category_embedding in category_embeddings.items():
        similarity = cosine_similarity(question_embedding.numpy().reshape(
            1, -1), category_embedding.reshape(1, -1))[0][0]
        similarities[category] = similarity

    sorted_categories = sorted(similarities.items(
    ), key=lambda x: x[1], reverse=True)[:3]  # Get top 3
    categories = [category.split("_")[0] for category, _ in sorted_categories]
    categories = list(dict.fromkeys(categories))
    return categories
