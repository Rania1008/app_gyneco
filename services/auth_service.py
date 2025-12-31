import hashlib
from models.user_model import UserModel

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate(username: str, password: str):
    user = UserModel.get_user_by_username(username)

    if not user:
        return None

    user_id, db_username, db_password, role = user
    if hash_password(password) == db_password:
        return {
            "id": user_id,
            "username": db_username,
            "role": role
        }

    return None
