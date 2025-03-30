import uuid
from psycopg2.extras import RealDictCursor
from config.config import get_db_connection
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
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        # Récupérer toutes les QAs avec une jointure pour inclure les MCQs
        cursor.execute("""
            SELECT 
                qa.id, qa.category, qa.question, qa.answer, qa.is_verified,
                qa_mcq.options, qa_mcq.justification
            FROM qa
            LEFT JOIN qa_mcq ON qa.id = qa_mcq.qa_id
        """)
        rows = cursor.fetchall()

        # Convertir les résultats en objets QA
        qas = [
            QA(
                id=row["id"],
                category=row["category"],
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
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        # Récupérer une QA avec une jointure pour inclure les MCQs
        cursor.execute("""
            SELECT 
                qa.id, qa.category, qa.question, qa.answer, qa.is_verified,
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
            category=row["category"],
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
        conn = get_db_connection()
        cursor = conn.cursor()

        # Mettre à jour la table `qa`
        cursor.execute(
            """
            UPDATE qa
            SET category = %s, question = %s, answer = %s, is_verified = %s
            WHERE id = %s
            """,
            (qa.category, qa.question, qa.answer, qa.is_verified, qa.id),
        )

        # Vérifier si la QA est un MCQ et mettre à jour ou insérer dans `qa_mcq`
        if qa.options and qa.justification:
            cursor.execute(
                """
                INSERT INTO qa_mcq (id, qa_id, options, justification)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (qa_id) DO UPDATE
                SET options = EXCLUDED.options, justification = EXCLUDED.justification
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
