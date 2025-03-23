from config.config import get_db_connection
import uuid
import psycopg2.extras

from api.services.auth_service import get_password_hash


def create_tables():
    psycopg2.extras.register_uuid()
    conn = get_db_connection()
    cursor = conn.cursor()

    # Supprimer les tables existantes sauf la table Users
    cursor.execute("DROP TABLE IF EXISTS qa_open CASCADE")
    cursor.execute("DROP TABLE IF EXISTS qa_mcq CASCADE")
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

    # Table QA (Questions and Answers)
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS qa (
            id UUID PRIMARY KEY,
            type VARCHAR(50) NOT NULL,
            category VARCHAR(50) NOT NULL,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            justification TEXT,
            is_verified BOOLEAN DEFAULT FALSE,
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS qa_mcq (
            id UUID PRIMARY KEY,
            qa_id UUID NOT NULL REFERENCES qa(id) ON DELETE CASCADE,
            options TEXT[] NOT NULL,
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
            url TEXT NOT NULL,
        )
        """
    )

    conn.commit()
    cursor.close()
    conn.close()


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


if __name__ == "__main__":
    create_tables()
    # create_admin_user()
    print("Tables créées avec succès et utilisateur administrateur ajouté.")
