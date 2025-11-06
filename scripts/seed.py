from app import app, db
from models.models import Usuario, UserCredentials, Categoria, Post, Comentario
from utils.security import hash_password

with app.app_context():
    db.create_all()
    if not Usuario.query.filter_by(email="admin@local").first():
        u1 = Usuario(nombre="admin", email="admin@local", role="admin", password=hash_password("adminpass"))
        db.session.add(u1)
        db.session.flush()
        db.session.add(UserCredentials(user_id=u1.id, password_hash=hash_password("adminpass")))

    if not Usuario.query.filter_by(email="mod@local").first():
        u2 = Usuario(nombre="moderador", email="mod@local", role="moderator", password=hash_password("modpass"))
        db.session.add(u2)
        db.session.flush()
        db.session.add(UserCredentials(user_id=u2.id, password_hash=hash_password("modpass")))

    if not Usuario.query.filter_by(email="user@local").first():
        u3 = Usuario(nombre="usuario", email="user@local", role="user", password=hash_password("userpass"))
        db.session.add(u3)
        db.session.flush()
        db.session.add(UserCredentials(user_id=u3.id, password_hash=hash_password("userpass")))

    if not Categoria.query.filter_by(nombre="General").first():
        c = Categoria(nombre="General")
        db.session.add(c)
        db.session.flush()
        admin = Usuario.query.filter_by(email="admin@local").first()
        p = Post(titulo="Bienvenido a la API", contenido="Primer post creado por seed", usuario_id=admin.id, categoria_id=c.id)
        db.session.add(p)
    db.session.commit()
    print("Seed ejecutado: admin@local/adminpass | mod@local/modpass | user@local/userpass")
