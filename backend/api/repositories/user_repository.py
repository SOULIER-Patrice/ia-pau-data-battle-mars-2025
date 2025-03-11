from uuid import UUID
from config.config import get_db_connection
from psycopg2.extras import RealDictCursor


def create_user(user: dict):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(
        """
        INSERT INTO users (id, email, first_name, last_name, roles, hashed_password)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (user['_id'], user['email'], user['first_name'],
         user['last_name'], user['roles'], user['hashed_password'])
    )
    conn.commit()
    cursor.close()
    conn.close()


def get_users():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return users


def find_user_by_email(email: str):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user


def find_user_by_id(user_id: UUID):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user


def update_user(user_id: UUID, user: dict):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(
        """
        UPDATE users
        SET email = %s, first_name = %s, last_name = %s, roles = %s, hashed_password = %s
        WHERE id = %s
        """,
        (user['email'], user['first_name'], user['last_name'],
         user['roles'], user['hashed_password'], user_id)
    )
    conn.commit()
    modified_count = cursor.rowcount
    cursor.close()
    conn.close()
    return modified_count


def delete_user(user_id: UUID):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()
    deleted_count = cursor.rowcount
    cursor.close()
    conn.close()
    return deleted_count
