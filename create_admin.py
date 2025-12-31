from services.auth_service import hash_password
from models.user_model import UserModel

UserModel.create_user(
    username="admin",
    password=hash_password("admin123"),
    role="admin"
)

print("✅ Utilisateur admin créé")
