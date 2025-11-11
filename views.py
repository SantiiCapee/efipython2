from datetime import timedelta
from flask import request, jsonify
from marshmallow import ValidationError
from flask.views import MethodView
from passlib.hash import bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from app import db
from models import Usuario, Post, Comentario, UserCredential
from schemas import UserRegisterSchema, LoginSchema, UserSchema, PostSchema, ComentarioSchema

# ---------- USERS ----------

userRegisterSchema = UserRegisterSchema()
loginSchema = LoginSchema()
userSchema = UserSchema()
usersSchema = UserSchema(many=True)

class UserAPI(MethodView):
    def get(self):
        users = Usuario.query.all()
        return usersSchema.dump(users), 200

    def post(self):
        # Crear usuario sin credenciales (no recomendado) — usamos /register para crear con password
        try:
            data = userSchema.load(request.json)
        except ValidationError as err:
            return {"errors": err.messages}, 400

        if Usuario.query.filter_by(email=data["email"]).first():
            return {"error": "Email ya registrado"}, 400

        new_user = Usuario(nombre=data["nombre"], email=data["email"])
        db.session.add(new_user)
        db.session.commit()
        return userSchema.dump(new_user), 201


class UserDetailAPI(MethodView):
    @jwt_required()
    def get(self, id):
        user = Usuario.query.get_or_404(id)
        return userSchema.dump(user), 200

    @jwt_required()
    def put(self, id):
        user = Usuario.query.get_or_404(id)
        try:
            data = userSchema.load(request.json)
        except ValidationError as err:
            return {"errors": err.messages}, 400

        # Solo mismo usuario o admin puede editar (chequeo básico)
        claims = get_jwt()
        requesterId = int(get_jwt_identity())
        role = claims.get("role")
        if requesterId != user.id and role != "admin":
            return {"error": "No autorizado"}, 403

        user.nombre = data["nombre"]
        user.email = data["email"]
        db.session.commit()
        return userSchema.dump(user), 200

    @jwt_required()
    def delete(self, id):
        user = Usuario.query.get_or_404(id)
        claims = get_jwt()
        requesterId = int(get_jwt_identity())
        role = claims.get("role")
        if requesterId != user.id and role != "admin":
            return {"error": "No autorizado"}, 403
        db.session.delete(user)
        db.session.commit()
        return {}, 204

# ---------- REGISTER / LOGIN ----------

class UserRegisterAPI(MethodView):
    def post(self):
        try:
            data = userRegisterSchema.load(request.json)
        except ValidationError as err:
            return {"errors": err.messages}, 400

        # verificar email único
        if Usuario.query.filter_by(email=data["email"]).first():
            return {"error": "Email en uso"}, 400

        # crear usuario (sin password en tabla Usuario)
        new_user = Usuario(nombre=data["nombre"], email=data["email"], role=data.get("role","user"))
        db.session.add(new_user)
        db.session.flush()  # para obtener new_user.id antes del commit
        password_hash = bcrypt.hash(data["password"])
        cred = UserCredential(user_id=new_user.id, password_hash=password_hash, role=data.get("role","user"))
        db.session.add(cred)
        db.session.commit()

        return userSchema.dump(new_user), 201

class LoginAPI(MethodView):
    def post(self):
        try:
            data = loginSchema.load(request.json)
        except ValidationError as err:
            return {"errors": err.messages}, 400

        user = Usuario.query.filter_by(email=data["email"]).first()
        if not user or not user.credentials:
            return {"error": "Usuario o credenciales no encontradas"}, 401

        if not bcrypt.verify(data["password"], user.credentials.password_hash):
            return {"error": "Credenciales inválidas"}, 401

        additional_claims = {
            "email": user.email,
            "role": user.credentials.role,
            "nombre": user.nombre
        }
        identity = str(user.id)
        token = create_access_token(identity=identity, additional_claims=additional_claims, expires_delta=timedelta(hours=8))
        return jsonify(access_token=token), 200

# ---------- POSTS mínimo para que no rompa ----------

postSchema = PostSchema()
postsSchema = PostSchema(many=True)

class PostsAPI(MethodView):
    def get(self):
        posts = Post.query.all()
        return postsSchema.dump(posts), 200

    @jwt_required()
    def post(self):
        try:
            data = postSchema.load(request.json)
        except ValidationError as err:
            return {"errors": err.messages}, 400

        user_id = int(get_jwt_identity())
        p = Post(titulo=data["titulo"], contenido=data["contenido"], usuario_id=user_id)
        db.session.add(p)
        db.session.commit()
        return postSchema.dump(p), 201

class PostDetailAPI(MethodView):
    def get(self, post_id):
        post = Post.query.get_or_404(post_id)
        return postSchema.dump(post), 200

    @jwt_required()
    def put(self, post_id):
        post = Post.query.get_or_404(post_id)
        try:
            data = postSchema.load(request.json, partial=True)
        except ValidationError as err:
            return {"errors": err.messages}, 400

        claims = get_jwt()
        requesterId = int(get_jwt_identity())
        role = claims.get("role")
        if requesterId != post.usuario_id and role != "admin":
            return {"error": "No autorizado"}, 403

        post.titulo = data.get("titulo", post.titulo)
        post.contenido = data.get("contenido", post.contenido)
        db.session.commit()
        return postSchema.dump(post), 200

    @jwt_required()
    def delete(self, post_id):
        post = Post.query.get_or_404(post_id)
        claims = get_jwt()
        requesterId = int(get_jwt_identity())
        role = claims.get("role")
        if requesterId != post.usuario_id and role != "admin":
            return {"error": "No autorizado"}, 403
        db.session.delete(post)
        db.session.commit()
        return {}, 204

# ---------- REVIEWS (COMENTARIOS) ----------        

comentarioSchema = ComentarioSchema()
comentariosSchema = ComentarioSchema(many=True)

class ReviewsAPI(MethodView):
    @jwt_required()
    def post(self):
        """Crear un comentario (review) para un post"""
        try:
            data = comentarioSchema.load(request.json)
        except ValidationError as err:
            return {"errors": err.messages}, 400

        user_id = int(get_jwt_identity())
        post_id = data["post_id"]
        texto = data["texto"]

        comentario = Comentario(texto=texto, usuario_id=user_id, post_id=post_id)
        db.session.add(comentario)
        db.session.commit()

        return comentarioSchema.dump(comentario), 201

    def get(self):
        """Listar todos los comentarios"""
        comentarios = Comentario.query.all()
        return comentariosSchema.dump(comentarios), 200


class ReviewDetailAPI(MethodView):
    @jwt_required()
    def get(self, review_id):
        comentario = Comentario.query.get_or_404(review_id)
        return comentarioSchema.dump(comentario), 200

    @jwt_required()
    def put(self, review_id):
        comentario = Comentario.query.get_or_404(review_id)
        claims = get_jwt()
        requesterId = int(get_jwt_identity())
        role = claims.get("role")

        if requesterId != comentario.usuario_id and role != "admin":
            return {"error": "No autorizado"}, 403

        data = request.get_json()
        comentario.texto = data.get("texto", comentario.texto)
        db.session.commit()
        return comentarioSchema.dump(comentario), 200

    @jwt_required()
    def delete(self, review_id):
        comentario = Comentario.query.get_or_404(review_id)
        claims = get_jwt()
        requesterId = int(get_jwt_identity())
        role = claims.get("role")

        if requesterId != comentario.usuario_id and role != "admin":
            return {"error": "No autorizado"}, 403

        db.session.delete(comentario)
        db.session.commit()
        return {}, 204