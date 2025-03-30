import yaml
import psycopg2
import psycopg2.extras
from ollama import Client

from ollama import Client
import requests.exceptions
import requests
import subprocess
import os
print("Chargement du fichier de configuration...")

# Charger le fichier de configuration
with open('config/config.yml', 'r') as file:
    config = yaml.safe_load(file)

print("Fichier de configuration chargé avec succès.")


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
    model_name = config['ai']['model']
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

    host = config['ai'].get('host', 'http://localhost:11434')  # Default host
    client = Client(host=host)
    print(f"Connexion à Ollama sur {host}")
    return client


def load_ai_config():
    model = config['ai']['model']
    max_output_tokens = config['ai']['max_output_tokens']
    model_classification = config['ai']['model_classification']
    model_rag = config['ai']['model_rag']

    return model, max_output_tokens, model_classification, model_rag


def get_db_connection(config_path='config/config.yml'):
    """
    Establishes and returns a database connection using psycopg2.

    Args:
        config_path (str): The path to the YAML configuration file.

    Yields:
        psycopg2.extensions.connection: A psycopg2 database connection object.
    """
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    if 'db' not in config:
        raise ValueError(
            f"'db' section not found in config file: {config_path}")

    psycopg2.extras.register_uuid()
    conn = psycopg2.connect(
        host=config['db']['host'],
        port=config['db']['port'],
        user=config['db']['user'],
        password=config['db']['password'],
        database=config['db']['database']
    )
    return conn  # Use yield to return the connection


ollama_client = get_ollama_client()
get_db_connection()
model, max_output_tokens, model_classification, model_rag = load_ai_config()
