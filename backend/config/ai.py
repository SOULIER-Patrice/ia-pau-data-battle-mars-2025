import config.initialization as init
from ollama import Client

def get_ollama_client():
    client = Client(
        init.config['ai']['host']
    )
    client.pull(init.config['ai']['model'])

    return client
# Connexion à la base de données

def load_ai_config():
    model = init.config['ai']['model']
    max_output_tokens = init.config['ai']['max_output_tokens']
    model_classification = init.config['ai']['model_classification']
    model_rag = init.config['ai']['model_rag']
    
    return model, max_output_tokens, model_classification, model_rag
    
print("test")
ollama_client = get_ollama_client()
model, max_output_tokens, model_classification, model_rag = load_ai_config()
