import yaml

from ollama import Client

from ollama import Client
import requests.exceptions
import requests
import subprocess

print("Chargement du fichier de configuration...")

# Charger le fichier de configuration
with open('config/config.yml', 'r') as file:
    config = yaml.safe_load(file)

print("Fichier de configuration chargé avec succès.")