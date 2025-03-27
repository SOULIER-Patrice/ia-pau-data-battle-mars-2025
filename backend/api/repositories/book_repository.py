import uuid
from psycopg2.extras import RealDictCursor

from config.config import get_db_connection

from typing import List, Optional
from api.models.Book import Book

def create_book(book_data: Book) -> uuid.UUID:
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(
        """
        INSERT INTO books (id, title, categories, type, user_id)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (
            book_data.id,
            book_data.title,
            book_data.categories,
            book_data.type,
            book_data.user_id,
        ),
    )
    conn.commit()
    cursor.close()
    conn.close()
    return book_data.id

def get_book(book_id: uuid.UUID) -> Optional[Book]:
    """
    Récupère un livre par son ID et retourne un objet Book.

    Args:
        book_id: L'ID du livre à récupérer.

    Returns:
        Un objet Book contenant les données du livre, ou None si le livre n'est pas trouvé.
    """
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(
        """
        SELECT * FROM books WHERE id = %s
        """,
        (str(book_id),),  # Convertir l'UUID en chaîne de caractères
    )

    book_data = cursor.fetchone()
    cursor.close()
    conn.close()

    if book_data:
        return Book(**book_data) # Create a Book object directly.
    else:
        return None

def get_books(user_id: uuid.UUID) -> List[Book]:
    """
    Récupère tous les livres associés à un utilisateur donné.

    Args:
        user_id: L'ID de l'utilisateur.

    Returns:
        Une liste d'objets Book contenant les données des livres.
    """
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(
        """
        SELECT * FROM books WHERE user_id = %s
        """,
        (str(user_id),),
    )
    books_data = cursor.fetchall()
    cursor.close()
    conn.close()

    if books_data:
        return [Book(**book_data) for book_data in books_data] #création de la liste d'objet book.
    else:
        return []