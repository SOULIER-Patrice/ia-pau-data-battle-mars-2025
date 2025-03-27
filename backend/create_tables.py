from config.config import get_db_connection
import uuid
import psycopg2.extras
import json
import os
import numpy as np

from api.services.auth_service import get_password_hash

from ai.src.models.classification import get_category_question


def create_tables():
    psycopg2.extras.register_uuid()
    conn = get_db_connection()
    cursor = conn.cursor()

    # Supprimer les tables existantes sauf la table Users
    cursor.execute("DROP TABLE IF EXISTS qa_mcq CASCADE")
    cursor.execute("DROP TABLE IF EXISTS qa CASCADE")
    cursor.execute("DROP TABLE IF EXISTS pages CASCADE")
    cursor.execute("DROP TABLE IF EXISTS books CASCADE")
    cursor.execute("DROP TABLE IF EXISTS articles CASCADE")

    # Table Users
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id UUID PRIMARY KEY,
            email VARCHAR(255) NOT NULL,
            first_name VARCHAR(255) NOT NULL,
            last_name VARCHAR(255) NOT NULL,
            roles TEXT[] NOT NULL,
            hashed_password VARCHAR(255) NOT NULL
        )
        """
    )

    # Table Books
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS books (
            id UUID PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            categories TEXT[] NOT NULL,
            type VARCHAR(50) NOT NULL,
            user_id UUID REFERENCES users(id) ON DELETE CASCADE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    # Table QA (Questions and Answers)
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS qa (
            id UUID PRIMARY KEY,
            type VARCHAR(50) NOT NULL,
            category VARCHAR(255) NOT NULL,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            is_verified BOOLEAN DEFAULT FALSE
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS qa_mcq (
            id UUID PRIMARY KEY,
            qa_id UUID NOT NULL REFERENCES qa(id) ON DELETE CASCADE,
            options TEXT[] NOT NULL,
            justification TEXT NOT NULL
        )
        """
    )

    # Table Pages
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS pages (
            id UUID PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            book_id UUID NOT NULL REFERENCES books(id) ON DELETE CASCADE,
            qa_id UUID REFERENCES qa(id) ON DELETE SET NULL,
            history JSONB NOT NULL DEFAULT '[]',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    # Table Articles
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS articles (
            id UUID PRIMARY KEY,
            type VARCHAR(50) NOT NULL,
            title VARCHAR(255) NOT NULL,
            url TEXT NOT NULL
        )
        """
    )

    # Commit and close connection
    conn.commit()
    cursor.close()
    conn.close()
    print("Tables created successfully!")


def create_admin_user():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Ajouter un utilisateur administrateur
    admin_id = uuid.uuid4()
    admin_email = "admin@example.com"
    admin_first_name = "Admin"
    admin_last_name = "User"
    admin_roles = ["admin"]
    admin_password = "password"
    admin_hashed_password = get_password_hash(admin_password)

    cursor.execute(
        """
        INSERT INTO users (id, email, first_name, last_name, roles, hashed_password)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING
        """,
        (admin_id, admin_email, admin_first_name,
         admin_last_name, admin_roles, admin_hashed_password)
    )

    conn.commit()
    cursor.close()
    conn.close()


def add_mcq_questions(question_dir, category_embeddings):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Vérifie si le chemin existe
    if not os.path.exists(question_dir):
        raise FileNotFoundError(f"Le dossier {question_dir} n'existe pas")

    # Récupération des fichiers MCQ et solutions
    mcq_files = sorted([f for f in os.listdir(
        question_dir) if f.endswith("_mcq.json")])
    solution_files = sorted([f for f in os.listdir(
        question_dir) if f.endswith("_mcq_solution.json")])
    # Parcours des fichiers MCQ et ajout à la base de données
    for i in range(len(mcq_files)):

        mcq_file = mcq_files[i]
        solution_file = solution_files[i]

        mcq_path = os.path.join(question_dir, mcq_file)
        solution_path = os.path.join(question_dir, solution_file)

        with open(mcq_path, 'r', encoding='utf-8') as f:
            mcq_data = json.load(f)

        with open(solution_path, 'r', encoding='utf-8') as f:
            solution_data = json.load(f)

        # Insérer les questions et solutions dans la base de données
        for qid, question_data in mcq_data.items():

            question = question_data["question"]
            answer = solution_data[qid]["Answer"]

            options = question_data["options"]
            justification = solution_data[qid]["Justification"]

            input = f"{question} {options}"
            category = get_category_question(input, category_embeddings)
            # Insérer la question dans la table qa
            cursor.execute(
                """
                INSERT INTO qa (id, type, category, question, answer, is_verified)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id
                """,
                (str(uuid.uuid4()), "MCQ", category, question, answer, True)
            )
            qa_id = cursor.fetchone()[0]

            # Insérer les options dans la table qa_mcq
            cursor.execute(
                """
                INSERT INTO qa_mcq (id, qa_id, options, justification)
                VALUES (%s, %s, %s, %s)
                """,
                (str(uuid.uuid4()), qa_id, options, justification)
            )

    # Commit et fermeture de la connexion
    conn.commit()
    cursor.close()
    conn.close()
    print("MCQ questions and solutions added successfully!")


def add_questions_open(question_dir, category_embeddings):

    conn = get_db_connection()
    cursor = conn.cursor()

    # Vérifie si le chemin existe
    if not os.path.exists(question_dir):
        raise FileNotFoundError(f"Le dossier {question_dir} n'existe pas")

    # Récupération des fichiers MCQ et solutions
    open_files = sorted([f for f in os.listdir(
        question_dir) if f.endswith("_open.json")])
    solution_files = sorted([f for f in os.listdir(
        question_dir) if f.endswith("_open_solution.json")])

    for i in range(len(open_files)):

        mcq_file = open_files[i]
        solution_file = solution_files[i]

        mcq_path = os.path.join(question_dir, mcq_file)
        solution_path = os.path.join(question_dir, solution_file)

        with open(mcq_path, 'r', encoding='utf-8') as f:
            mcq_data = json.load(f)

        with open(solution_path, 'r', encoding='utf-8') as f:
            solution_data = json.load(f)

        # Insérer les questions et solutions dans la base de données
        for qid, question_data in mcq_data.items():

            question = question_data.strip()
            answer = solution_data[qid].strip()
            # Insérer la question dans la table qa
            input = f"{question}"
            category = get_category_question(input, category_embeddings)
            cursor.execute(
                """
                INSERT INTO qa (id, type, category, question, answer, is_verified)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id
                """,
                (str(uuid.uuid4()), "OPEN", category, question, answer, True)
            )
    # Commit et fermeture de la connexion
    conn.commit()
    cursor.close()
    conn.close()
    print("Open questions and solutions added successfully!!")


if __name__ == "__main__":
    create_tables()
    # create_admin_user()
    question_dir = os.path.abspath('./ai/outputs')

    category_embeddings = np.load(
        './ai/embeddings/categories_bert-base-uncased-eurlex.npy', allow_pickle=True).item()

    add_mcq_questions(question_dir, category_embeddings)
    add_questions_open(question_dir, category_embeddings)
    print("Tables créées avec succès et utilisateur administrateur ajouté.")
