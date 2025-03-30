import config.initialization as init
import psycopg2
import psycopg2.extras

def get_db_connection():
    """
    Establishes and returns a database connection using psycopg2.

    Args:
        initialization.config_path (str): The path to the YAML initialization.configuration file.

    Yields:
        psycopg2.extensions.connection: A psycopg2 database connection object.
    """
    psycopg2.extras.register_uuid()
    conn = psycopg2.connect(
        host=init.config['db']['host'],
        port=init.config['db']['port'],
        user=init.config['db']['user'],
        password=init.config['db']['password'],
        database=init.config['db']['database']
    )
    return conn  # Use yield to return the connection