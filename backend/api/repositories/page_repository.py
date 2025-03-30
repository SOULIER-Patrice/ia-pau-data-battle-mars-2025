import uuid
from psycopg2.extras import RealDictCursor
import config.db_connect as db_connect
import psycopg2
from typing import List, Dict
from api.models.QA import QA
from api.models.Page import Page, PageForCreate
import json


def create_page(page_for_create: PageForCreate) -> uuid.UUID:
    """
    Crée une nouvelle page et retourne son ID.
    """
    conn = None
    cursor = None
    try:
        conn = db_connect.get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        cursor.execute(
            """
            INSERT INTO pages (id, title, book_id, qa_id)
            VALUES (%s, %s, %s, %s)
            """,
            (
                page_for_create.id,
                page_for_create.title,
                page_for_create.book_id,
                page_for_create.qa_id,
            ),
        )

        conn.commit()
        # return the id that was given to the function.
        return page_for_create.id

    except psycopg2.Error as e:
        if conn:
            conn.rollback()
        print(f"Erreur de base de données : {e}")
        return None

    except KeyError as e:
        print(f"Erreur de clef de donnée : {e}")
        return None

    except Exception as e:
        print(f"Erreur Inattendue : {e}")
        return None

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def update_page_history(page_id: uuid.UUID, history: list) -> bool:
    """
    Met à jour l'historique d'une page dans la base de données.

    Args:
        page_id: L'ID de la page à mettre à jour.
        history: La nouvelle liste d'historique.

    Returns:
        True si la mise à jour réussit, False sinon.
    """
    conn = None
    cursor = None
    try:
        conn = db_connect.get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        # Convertir la liste d'historique en JSONB
        history_json = json.dumps(history)

        cursor.execute(
            """
            UPDATE pages
            SET history = %s
            WHERE id = %s
            """,
            (history_json, str(page_id)),
        )

        conn.commit()
        return True

    except psycopg2.Error as e:
        if conn:
            conn.rollback()
        print(
            f"Erreur de base de données lors de la mise à jour de l'historique : {e}")
        return False

    except Exception as e:
        print(
            f"Erreur inattendue lors de la mise à jour de l'historique : {e}")
        return False

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_page(page_id: uuid.UUID) -> Page:
    """
    Récupère une page par son ID, incluant le qa_id.

    Args:
        page_id: L'ID de la page à récupérer.

    Returns:
        Un objet Page contenant les données de la page, ou None si la page n'est pas trouvée.
    """
    conn = db_connect.get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(
        """
        SELECT id, title, book_id, history, created_at, qa_id FROM pages WHERE id = %s
        """,
        (str(page_id),),
    )
    page_data = cursor.fetchone()
    cursor.close()
    conn.close()

    return Page(**page_data)


def get_pages(book_id: uuid.UUID) -> List[Page]:
    """
    Récupère toutes les pages associées à un livre donné.

    Args:
        book_id: L'ID du livre.

    Returns:
        Une liste d'objets Page contenant les données des pages, ou une liste vide si aucune page n'est trouvée.
    """
    conn = db_connect.get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(
        """
        SELECT id, title, book_id, history, created_at, qa_id FROM pages WHERE book_id = %s
        """,
        (str(book_id),),  # Convertir l'UUID en chaîne de caractères
    )
    pages_data = cursor.fetchall()
    cursor.close()
    conn.close()

    if pages_data:
        return [Page(**page_data) for page_data in pages_data]
    else:
        return []
