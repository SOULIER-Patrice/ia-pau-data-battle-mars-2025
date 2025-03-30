import uuid
from psycopg2.extras import RealDictCursor
import config.db_connect as db_connect
import psycopg2
from typing import List, Dict
from api.models.Page import Page, QA, PageForCreate
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
        return page_for_create.id # return the id that was given to the function.

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
        print(f"Erreur de base de données lors de la mise à jour de l'historique : {e}")
        return False

    except Exception as e:
        print(f"Erreur inattendue lors de la mise à jour de l'historique : {e}")
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


def create_qa_open(category: str, question: str, answer: str) -> uuid.UUID:
    """
    Crée une question de type OPEN et retourne son ID.

    Args:
        category: La catégorie de la question.
        question: Le texte de la question.
        answer: La réponse à la question.

    Returns:
        L'ID de la question créée.
    """
    conn = db_connect.get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    qa_id = str(uuid.uuid4())
    cursor.execute(
        """
        INSERT INTO qa (id, type, category, question, answer, is_verified)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (qa_id, "OPEN", category, question, answer, False),
    )

    conn.commit()
    cursor.close()
    conn.close()
    return qa_id


def create_qa_mcq(category: str, question_data: Dict[str, str], answer_data: Dict[str, str]) -> uuid.UUID:
    """
    Crée une question de type MCQ et retourne son ID.
    """
    try:
        conn = db_connect.get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        qa_id = str(uuid.uuid4())

        cursor.execute(
            """
            INSERT INTO qa (id, type, category, question, answer, is_verified)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (qa_id, "MCQ", category, question_data["question"], answer_data["Answer"], False),
        )

        cursor.execute(
            """
            INSERT INTO qa_mcq (id, qa_id, options, justification)
            VALUES (%s, %s, %s, %s)
            """,
            (str(uuid.uuid4()), qa_id, question_data["options"], answer_data["Justification"]),
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



def get_qa(qa_id: uuid.UUID) -> QA:
    """
    Récupère une question/réponse (QA) par son ID.

    Args:
        qa_id: L'ID de la QA à récupérer.

    Returns:
        Un dictionnaire contenant les données de la QA, ou None si la QA n'est pas trouvée.
    """
    conn = db_connect.get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    # Récupérer les données de la table 'qa'
    cursor.execute(
        """
        SELECT id, category, question, answer, is_verified FROM qa WHERE id = %s
        """,
        (str(qa_id),),
    )
    qa_data = cursor.fetchone()

    if qa_data:
        # Récupérer les données de la table 'qa_mcq' si elles existent
        cursor.execute(
            """
            SELECT options, justification FROM qa_mcq WHERE qa_id = %s
            """,
            (str(qa_id),),
        )
        mcq_data = cursor.fetchone()

        if mcq_data:
            # Combiner les données de 'qa' et 'qa_mcq'
            qa_data.update(mcq_data)

        cursor.close()
        conn.close()
        return qa_data
    else:
        cursor.close()
        conn.close()
        return None
    

def get_qa_by_category(category: str, is_verified: bool = True) -> List[QA]:
    """
    Récupère une question/réponse (QA) par sa catégorie, en filtrant par le champ is_verified.

    Args:
        category: La catégorie de la QA à récupérer.
        is_verified: Filtre les QA en fonction de leur état de vérification (True par défaut).

    Returns:
        Une liste d'objets QA contenant les données des QAs, ou une liste vide si aucune QA n'est trouvée pour cette catégorie.
    """
    conn = db_connect.get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    # Récupérer les données de la table 'qa' en filtrant par catégorie et is_verified
    cursor.execute(
        """
        SELECT id, category, question, answer, is_verified FROM qa WHERE category = %s AND is_verified = %s
        """,
        (category, is_verified),
    )
    qa_data = cursor.fetchall()  # Récupérer toutes les QA correspondantes

    if qa_data:
        qa_list = []
        for qa in qa_data:
            # Récupérer les données de la table 'qa_mcq' si elles existent
            cursor.execute(
                """
                SELECT options, justification FROM qa_mcq WHERE qa_id = %s
                """,
                (qa['id'],),
            )
            mcq_data = cursor.fetchone()

            if mcq_data:
                # Combiner les données de 'qa' et 'qa_mcq'
                qa.update(mcq_data)

            qa_list.append(QA(**qa)) # ajouter l'objet qa a la list.
        cursor.close()
        conn.close()
        return qa_list  # Retourner la liste des QA
    else:
        cursor.close()
        conn.close()
        return []
    