import yaml
import psycopg2
import psycopg2.extras
from ollama import Client
print("Chargement du fichier de configuration...")

# Charger le fichier de configuration
with open('config/config.yml', 'r') as file:
    config = yaml.safe_load(file)

print("Fichier de configuration chargé avec succès.")

def get_ollama_client():
    ollama_client.pull(config['ai']['model'])
    client = Client(
        config['ai']['host']
    )
    return client
# Connexion à la base de données

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
        raise ValueError(f"'db' section not found in config file: {config_path}")

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
