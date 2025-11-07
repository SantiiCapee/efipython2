from models.models import Usuario, UserCredentials, db

class UserRepository:
    @staticmethod
    def get_by_id(user_id):
        return Usuario.query.get(user_id)

    @staticmethod
    def get_by_email(email):
        return Usuario.query.filter_by(email=email).first()

    @staticmethod
    def create_user(nombre, email, password_hash, role='user'):
        user = Usuario(nombre=nombre, email=email, role=role, password=password_hash)
        db.session.add(user)
        db.session.flush()
        cred = UserCredentials(user_id=user.id, password_hash=password_hash)
        db.session.add(cred)
        db.session.commit()
        return user

    @staticmethod
    def list_all():
        return Usuario.query.all()

    @staticmethod
    def update_role(user_id, new_role):
        user = Usuario.query.get_or_404(user_id)
        user.role = new_role
        db.session.commit()
        return user

    @staticmethod
    def deactivate(user_id):
        user = Usuario.query.get_or_404(user_id)
        user.is_active = False
        db.session.commit()
        return user
    
    @staticmethod
    def update_user(user_id, role=None, is_active=None):
        user = Usuario.query.get_or_404(user_id)
        if role:
            user.role = role
        if is_active is not None:
            user.is_active = is_active
        db.session.commit()
        return user
