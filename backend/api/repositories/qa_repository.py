import uuid
from psycopg2.extras import RealDictCursor
import config.db_connect as db_connect
import psycopg2
from typing import List

from api.models.QA import QA


def get_qas() -> List[QA]:
    """
    Récupère toutes les QAs de la base de données, y compris les options et justifications pour les QAs MCQ.
    """
    conn = None
    cursor = None
    try:
        conn = db_connect.get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        # Récupérer toutes les QAs avec une jointure pour inclure les MCQs
        cursor.execute("""
            SELECT 
                qa.id, qa.type, qa.categories, qa.question, qa.answer, qa.is_verified,
                qa_mcq.options, qa_mcq.justification
            FROM qa
            LEFT JOIN qa_mcq ON qa.id = qa_mcq.qa_id
        """)
        rows = cursor.fetchall()

        # Convertir les résultats en objets QA
        qas = [
            QA(
                id=row["id"],
                type=row["type"],
                categories=row["categories"],
                question=row["question"],
                answer=row["answer"],
                is_verified=row["is_verified"],
                options=row["options"],
                justification=row["justification"]
            )
            for row in rows
        ]

        return qas

    except psycopg2.Error as e:
        if conn:
            conn.rollback()
        print(f"Erreur de base de données : {e}")
        return []

    except Exception as e:
        print(f"Erreur Inattendue : {e}")
        return []

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_qa(qa_id: uuid.UUID) -> QA:
    """
    Récupère une QA spécifique de la base de données, y compris les options et justifications pour les QAs MCQ.
    """
    conn = None
    cursor = None
    try:
        conn = db_connect.get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        # Récupérer une QA avec une jointure pour inclure les MCQs
        cursor.execute("""
            SELECT 
                qa.id, qa.type, qa.categories, qa.question, qa.answer, qa.is_verified,
                qa_mcq.options, qa_mcq.justification
            FROM qa
            LEFT JOIN qa_mcq ON qa.id = qa_mcq.qa_id
            WHERE qa.id = %s
        """, (qa_id,))
        row = cursor.fetchone()

        if not row:
            return None

        # Convertir le résultat en objet QA
        return QA(
            id=row["id"],
            type=row["type"],
            categories=row["categories"],
            question=row["question"],
            answer=row["answer"],
            is_verified=row["is_verified"],
            options=row["options"],
            justification=row["justification"]
        )

    except psycopg2.Error as e:
        if conn:
            conn.rollback()
        print(f"Erreur de base de données : {e}")
        return None

    except Exception as e:
        print(f"Erreur Inattendue : {e}")
        return None

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def update_qa(qa: QA) -> bool:
    """
    Met à jour une QA dans la base de données, y compris les options et justifications pour les QAs MCQ.
    """
    conn = None
    cursor = None
    try:
        conn = db_connect.get_db_connection()
        cursor = conn.cursor()

        # Mettre à jour la table `qa`
        cursor.execute(
            """
            UPDATE qa
            SET categories = %s, question = %s, answer = %s, is_verified = %s
            WHERE id = %s
            """,
            (qa.categories, qa.question, qa.answer, qa.is_verified, qa.id),
        )

        # Vérifier si la QA est un MCQ et mettre à jour ou insérer dans `qa_mcq`
        if qa.options and qa.justification:
            cursor.execute(
                """
                INSERT INTO qa_mcq (id, qa_id, options, justification)
                VALUES (%s, %s, %s, %s);
                """,
                (uuid.uuid4(), qa.id, qa.options, qa.justification),
            )
        else:
            # Si ce n'est pas un MCQ, supprimer l'entrée correspondante dans `qa_mcq`
            cursor.execute("DELETE FROM qa_mcq WHERE qa_id = %s", (qa.id,))

        conn.commit()
        return True

    except psycopg2.Error as e:
        if conn:
            conn.rollback()
        print(f"Erreur de base de données : {e}")
        return False

    except Exception as e:
        print(f"Erreur Inattendue : {e}")
        return False

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_qas_by_category(category: str, type: str, is_verified: bool = True) -> List[QA]:
    """
    Récupère une question/réponse (QA) par sa catégorie, en filtrant par le champ is_verified.

    Args:
        category: La catégorie de la QA à récupérer.
        is_verified: Filtre les QA en fonction de leur état de vérification (True par défaut).

    Returns:
        Une liste d'objets QA contenant les données des QAs, ou une liste vide si aucune QA n'est trouvée pour cette catégorie.
    """

    """
    Récupère toutes les QAs de la base de données, y compris les options et justifications pour les QAs MCQ.
    """
    conn = None
    cursor = None
    try:
        conn = db_connect.get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        # Récupérer toutes les QAs avec une jointure pour inclure les MCQs
        cursor.execute("""
            SELECT 
                qa.id, qa.type, qa.categories, qa.question, qa.answer, qa.is_verified,
                qa_mcq.options, qa_mcq.justification
            FROM qa
            LEFT JOIN qa_mcq ON qa.id = qa_mcq.qa_id
            WHERE  %s = ANY(qa.categories) AND qa.type = %s AND qa.is_verified = %s
        """, (category, type, is_verified))
        rows = cursor.fetchall()

        # Convertir les résultats en objets QA
        qas = [
            QA(
                id=row["id"],
                type=row["type"],
                categories=row["categories"],
                question=row["question"],
                answer=row["answer"],
                is_verified=row["is_verified"],
                options=row["options"],
                justification=row["justification"]
            )
            for row in rows
        ]

        return qas

    except psycopg2.Error as e:
        if conn:
            conn.rollback()
        print(f"Erreur de base de données : {e}")
        return []

    except Exception as e:
        print(f"Erreur Inattendue : {e}")
        return []

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_qas_by_book(book_id: uuid.UUID) -> List[QA]:
    """
    Retrieves all QAs associated with a specific book.

    Args:
        book_id: The UUID of the book.

    Returns:
        A list of QA objects associated with the book.
    """
    conn = None
    cursor = None
    try:

        conn = db_connect.get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(
            """SELECT qa.id, qa.type, qa.categories, qa.question, qa.answer, qa.is_verified, qa_mcq.options, qa_mcq.justification
            FROM qa
            LEFT JOIN qa_mcq ON qa.id = qa_mcq.qa_id
            JOIN pages ON qa.id = pages.qa_id
            WHERE pages.book_id = %s""", (str(book_id),))  # Convert UUID to string for the query
        rows = cursor.fetchall()

        # Convertir les résultats en objets QA
        qas = [
            QA(
                id=row["id"],
                type=row["type"],
                categories=row["categories"],
                question=row["question"],
                answer=row["answer"],
                is_verified=row["is_verified"],
                options=row["options"],
                justification=row["justification"]
            )
            for row in rows
        ]

        return qas

    except psycopg2.Error as e:
        if conn:
            conn.rollback()
        print(f"Erreur de base de données : {e}")
        return []

    except Exception as e:
        print(f"Erreur Inattendue : {e}")
        return []

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def create_qa_open(categories: list[str], question: str, answer: str) -> uuid.UUID:
    """
    Crée une question de type OPEN et retourne son ID.

    Args:
        categories: La catégorie de la question.
        question: Le texte de la question.
        answer: La réponse à la question.

    Returns:
        L'ID de la question créée.
    """
    conn = None
    cursor = None
    try:

        conn = db_connect.get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        qa_id = str(uuid.uuid4())
        cursor.execute(
            """
            INSERT INTO qa (id, type, categories, question, answer, is_verified)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (qa_id, "OPEN", categories, question, answer, False),
        )

        conn.commit()
        return qa_id

    except psycopg2.Error as e:
        if conn:
            conn.rollback()
        print(f"Erreur de base de données : {e}")
        return []

    except Exception as e:
        print(f"Erreur Inattendue : {e}")
        return []

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def create_qa_mcq(categories: list[str], question: str, answer: str, options: str, justification: str) -> uuid.UUID:
    """
    Crée une question de type MCQ et retourne son ID.
    """
    try:
        conn = db_connect.get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        qa_id = str(uuid.uuid4())

        cursor.execute(
            """
            INSERT INTO qa (id, type, categories, question, answer, is_verified)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (qa_id, "MCQ", categories,
             question, answer, False),
        )

        cursor.execute(
            """
            INSERT INTO qa_mcq (id, qa_id, options, justification)
            VALUES (%s, %s, %s, %s)
            """,
            (str(uuid.uuid4()), qa_id,
             options, justification),
        )

        conn.commit()
        return qa_id

    except psycopg2.Error as e:
        if conn:
            conn.rollback()
        print(f"Erreur de base de données : {e}")
        return None  # Ou lancez l'exception, selon votre gestion des erreurs

    except Exception as e:
        print(f"Erreur Inattendue : {e}")
        return None

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
