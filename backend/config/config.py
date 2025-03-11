import yaml
import psycopg2
import psycopg2.extras

print("Chargement du fichier de configuration...")

# Charger le fichier de configuration
with open('config/config.yml', 'r') as file:
    config = yaml.safe_load(file)

print("Fichier de configuration chargé avec succès.")

# Connexion à la base de données


def get_db_connection():
    psycopg2.extras.register_uuid()
    conn = psycopg2.connect(
        host=config['db']['host'],
        port=config['db']['port'],
        user=config['db']['user'],
        password=config['db']['password'],
        database=config['db']['database']
    )
    return conn
