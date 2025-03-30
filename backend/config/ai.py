import config.initialization as init
from ollama import Client
import os
import subprocess

def check_model_exists(model_name):
    """Vérifie si le modèle existe localement."""
    model_path = os.path.expanduser(f"~/.ollama/models/{model_name}")
    return os.path.exists(model_path)


def download_model(model_name):
    """Télécharge le modèle avec Ollama."""
    try:
        subprocess.run(["ollama", "pull", model_name], check=True)
        print(f"Modèle {model_name} téléchargé avec succès.")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors du téléchargement du modèle : {e}")
        return False
    return True


def init_ollama_model():
    model_name = init.config['ai']['model']
    if not check_model_exists(model_name):
        print(
            f"Le modèle {model_name} n'existe pas localement. Téléchargement en cours...")
        if not download_model(model_name):
            raise Exception(
                f"Le téléchargement du modèle {model_name} a échoué.")
        else:
            print(f"Le modèle {model_name} a été téléchargé avec succès.")


def get_ollama_client():
    """Initialise le client Ollama et télécharge le modèle si nécessaire."""

    host = init.config['ai'].get('host', 'http://localhost:11434')  # Default host
    client = Client(host=host)
    print(f"Connexion à Ollama sur {host}")
    return client


# Connexion à la base de données

def load_ai_config():
    model = init.config['ai']['model']
    max_output_tokens = init.config['ai']['max_output_tokens']
    model_classification = init.config['ai']['model_classification']
    model_rag = init.config['ai']['model_rag']
    
    return model, max_output_tokens, model_classification, model_rag
    
ollama_client = get_ollama_client()
model, max_output_tokens, model_classification, model_rag = load_ai_config()
