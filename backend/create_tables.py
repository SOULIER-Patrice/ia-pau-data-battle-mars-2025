from config.config import get_db_connection
import uuid
import hashlib
import psycopg2.extras

from api.services.auth_service import get_password_hash


def create_tables():
    psycopg2.extras.register_uuid()
    conn = get_db_connection()
    cursor = conn.cursor()
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
    conn.commit()

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
        """,
        (admin_id, admin_email, admin_first_name,
         admin_last_name, admin_roles, admin_hashed_password)
    )
    conn.commit()

    cursor.close()
    conn.close()


if __name__ == "__main__":
    create_tables()
    print("Tables créées avec succès et utilisateur administrateur ajouté.")
