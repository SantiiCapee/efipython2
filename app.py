import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

load_dotenv()

app = Flask(__name__)

# Configuración DB
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI", "mysql+pymysql://root:@localhost/db_blogcito")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = os.getenv("SECRET_KEY", "dev_secret_key")

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager

ma = Marshmallow(app)
app.config.setdefault('JWT_SECRET_KEY', os.getenv('JWT_SECRET_KEY', 'jwt_dev_secret'))
app.config.setdefault('JWT_ACCESS_TOKEN_EXPIRES', 86400)  # 24 horas
jwt = JWTManager(app)

from models.models import Usuario, Post, Comentario, Categoria, UserCredentials

@app.context_processor
def inject_categorias():
    try:
        categorias = Categoria.query.all()
    except Exception:
        categorias = []
    return dict(categorias=categorias)

#VISTAS WEB 

@app.route("/")
def index():
    posts = Post.query.order_by(Post.fecha_creacion.desc()).all()
    # Si no existe el tmplate devuelve un texto simple
    try:
        return render_template("index.html", posts=posts)
    except Exception:
        return "<h1>Index</h1><p>Posts: {}</p>".format(len(posts))

@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nombre = request.form["nombre"].strip()
        email = request.form["email"].strip()
        password = request.form["password"].strip()

        if not nombre or not email or not password:
            flash('Por favor complete todos los campos.', 'danger')
            return redirect(url_for('registro'))

        if Usuario.query.filter_by(nombre=nombre).first():
            flash('El nombre de usuario ya existe, por favor elija otro.', 'danger')
            return redirect(url_for('registro'))

        if Usuario.query.filter_by(email=email).first():
            flash('El correo ya está registrado.', 'danger')
            return redirect(url_for('registro'))

        from utils.security import hash_password
        password_hash = hash_password(password)

        usuario = Usuario(nombre=nombre, email=email, password=password_hash)
        db.session.add(usuario)
        db.session.flush()
        cred = UserCredentials(user_id=usuario.id, password_hash=password_hash)
        db.session.add(cred)
        db.session.commit()

        session["usuario_id"] = usuario.id
        session["usuario_nombre"] = usuario.nombre

        flash(f'Bienvenido, {usuario.nombre}! Tu cuenta fue creada con éxito.', 'success')
        return redirect(url_for("index"))

    try:
        return render_template("registro.html")
    except Exception:
        return "<h1>Registro</h1>"

@app.route("/nuevo_post", methods=["GET", "POST"])
def nuevo_post():
    if "usuario_id" not in session:
        flash("Debes iniciar sesión para crear un post.", "danger")
        return redirect(url_for("login"))
    if request.method == "POST":
        titulo = request.form["titulo"]
        contenido = request.form["contenido"]
        categoria_id = request.form.get("categoria_id") or 1

        post = Post(titulo=titulo, contenido=contenido, usuario_id=session["usuario_id"], categoria_id=categoria_id)
        db.session.add(post)
        db.session.commit()
        flash("Post creado con éxito.", "success")
        return redirect(url_for("index"))
    try:
        return render_template("nuevo_post.html")
    except Exception:
        return "<h1>Nuevo Post</h1>"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip()
        password = request.form["password"].strip()

        usuario = Usuario.query.filter_by(email=email).first()
        if not usuario:
            flash("Correo o contraseña incorrectos.", "danger")
            return redirect(url_for("login"))

        from utils.security import verify_password
        cred = UserCredentials.query.filter_by(user_id=usuario.id).first()
        valid = False
        if cred:
            valid = verify_password(cred.password_hash, password)
        elif usuario.password:
            valid = verify_password(usuario.password, password)

        if usuario and valid:
            session["usuario_id"] = usuario.id
            session["usuario_nombre"] = usuario.nombre
            flash(f"Bienvenido {usuario.nombre}!", "success")
            return redirect(url_for("index"))
        else:
            flash("Correo o contraseña incorrectos.", "danger")
            return redirect(url_for("login"))

    try:
        return render_template("login.html")
    except Exception:
        return "<h1>Login</h1>"

@app.route("/logout")
def logout():
    session.clear()
    flash("Has cerrado sesión.", "info")
    return redirect(url_for("index"))

@app.route("/post/<int:post_id>", methods=["GET", "POST"])
def ver_post(post_id):
    post = Post.query.get_or_404(post_id)

    if request.method == "POST":
        if "usuario_id" not in session:
            flash("Debes iniciar sesión para comentar.", "danger")
            return redirect(url_for("login"))

        texto = request.form["texto"].strip()
        if not texto:
            flash("El comentario no puede estar vacío.", "danger")
            return redirect(url_for("ver_post", post_id=post_id))

        comentario = Comentario(
            texto=texto,
            usuario_id=session["usuario_id"],
            post_id=post.id
        )
        db.session.add(comentario)
        db.session.commit()

        flash("Comentario agregado con éxito.", "success")
        return redirect(url_for("ver_post", post_id=post_id))

    try:
        return render_template("post_detalle.html", post=post)
    except Exception:
        return f"<h1>{post.titulo}</h1><p>{post.contenido}</p>"

try:
    from routes.auth_routes import auth_bp
    from routes.post_routes import post_bp
    from routes.comment_routes import comment_bp
    from routes.category_routes import category_bp
    from routes.user_routes import user_bp
    from routes.stats_routes import stats_bp

    app.register_blueprint(auth_bp, url_prefix="/api")
    app.register_blueprint(post_bp, url_prefix="/api")
    app.register_blueprint(comment_bp, url_prefix="/api")
    app.register_blueprint(category_bp, url_prefix="/api")
    app.register_blueprint(user_bp, url_prefix="/api")
    app.register_blueprint(stats_bp, url_prefix="/api")
except Exception as e:
    print("Aviso: blueprints API no cargados. Error:", e)

if __name__ == "__main__":
    app.run(debug=True)
