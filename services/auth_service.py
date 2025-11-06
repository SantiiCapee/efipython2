from repositories.user_repository import UserRepository
from utils.security import hash_password, verify_password
from models.models import UserCredentials

class AuthService:
    def register(self, nombre, email, password):
        existing = UserRepository.get_by_email(email)
        if existing:
            raise ValueError("Email ya registrado")
        pwd_hash = hash_password(password)
        user = UserRepository.create_user(nombre, email, pwd_hash)
        return user

    def authenticate(self, email, password):
        user = UserRepository.get_by_email(email)
        if not user:
            return None
        cred = UserCredentials.query.filter_by(user_id=user.id).first()
        if cred and verify_password(cred.password_hash, password):
            return user
        # fallback to legacy column
        if user.password and verify_password(user.password, password):
            return user
        return None
