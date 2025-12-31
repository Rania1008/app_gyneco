from config.database import get_connection

class UserModel:

    @staticmethod
    def get_user_by_username(username):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, username, password, role FROM users WHERE username = ?",
            (username,)
        )

        user = cursor.fetchone()
        conn.close()
        return user

    @staticmethod
    def create_user(username, password, role):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (username, password, role)
        )

        conn.commit()
        conn.close()
