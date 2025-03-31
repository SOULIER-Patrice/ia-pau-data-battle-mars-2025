import os
import config.ai as ai
import config.db_connect as db_connect
import numpy as np

from ai.src.create_embeddings import create_classification_embeddings, create_rag_embeddings, add_classification_question
from create_tables import create_tables, add_mcq_questions, add_questions_open


data_dir = os.path.abspath('data')
output_dir = os.path.abspath('ai/embeddings')

# Créer le dossier de sortie s'il n'existe pas
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Appel de la fonction pour créer les embeddings
create_classification_embeddings(
    ai.model_classification, data_dir, output_dir)

category_embeddings = np.load(
    f"{output_dir}/categories_{ai.model_classification.split('/')[-1]}.npy", allow_pickle=True).item()

if ai.remake_classification:
    add_classification_question(
        ai.model_classification, category_embeddings, data_dir)


markdown_separators = [
    "\n\n",
    "\n",
    ".",
    " ",
    "",
]

data_dir = os.path.abspath('data')
output_dir = os.path.abspath('ai/embeddings')

# Créer le dossier de sortie s'il n'existe pas
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

create_rag_embeddings(ai.model_rag, markdown_separators,
                      data_dir, output_dir, device=ai.device)


def table_exists(conn, table_name):
    """
    Checks if a table exists in the database.
    """
    cursor = conn.cursor()
    cursor.execute("""
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_name = %s
        );
    """, (table_name,))
    return cursor.fetchone()[0]


question_dir = f"{data_dir}/qa"
conn = db_connect.get_db_connection()
if not table_exists(conn, "qa") or db_connect.reset_db:
    create_tables()

    add_mcq_questions(question_dir)
    add_questions_open(question_dir)

elif ai.remake_classification:
    add_mcq_questions(question_dir)
    add_questions_open(question_dir)
