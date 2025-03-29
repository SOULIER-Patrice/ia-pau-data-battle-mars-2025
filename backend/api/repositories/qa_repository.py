import uuid
from psycopg2.extras import RealDictCursor
from config.config import get_db_connection
import psycopg2
from typing import List

from api.models.Page import QA


def get_qas() -> List[QA]:
    """
    Récupère toutes les QAs de la base de données.
    """
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        cursor.execute("SELECT * FROM qa")
        rows = cursor.fetchall()

        return rows

    except psycopg2.Error as e:
        if conn:
            conn.rollback()
        print(f"Erreur de base de données : {e}")
        return []

    except KeyError as e:
        print(f"Erreur de clef de donnée : {e}")
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
    Récupère une QA spécifique de la base de données.
    """
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        cursor.execute("SELECT * FROM qa WHERE id = %s", (qa_id,))
        row = cursor.fetchone()

        return row

    except psycopg2.Error as e:
        if conn:
            conn.rollback()
        print(f"Erreur de base de données : {e}")
        return {}

    except KeyError as e:
        print(f"Erreur de clef de donnée : {e}")
        return {}

    except Exception as e:
        print(f"Erreur Inattendue : {e}")
        return {}

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def update_qa(qa: QA) -> bool:
    """
    Met à jour une QA dans la base de données.
    """
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE qa
            SET question = %s, answer = %s, is_verified = %s
            WHERE id = %s
            """,
            (qa.question, qa.answer, qa.is_verified, qa.id),
        )

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


def delete_qa(qa_id: uuid.UUID) -> bool:
    """
    Supprime une QA de la base de données.
    """
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM qa WHERE id = %s", (qa_id,))

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
