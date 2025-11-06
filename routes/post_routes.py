from flask import Blueprint, request, jsonify
from flask.views import MethodView
from services.post_service import PostService
from models.models import Post
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from repositories.user_repository import UserRepository

post_bp = Blueprint("post", __name__)
post_service = PostService()

class PostsAPI(MethodView):
    def get(self):
        posts = post_service.get_public_posts()
        result = [{
            "id": p.id,
            "titulo": p.titulo,
            "contenido": p.contenido,
            "usuario_id": p.usuario_id,
            "fecha_creacion": p.fecha_creacion.isoformat()
        } for p in posts]
        return jsonify(result), 200

    @jwt_required()
    def post(self):
        data = request.get_json() or {}
        titulo = data.get("titulo")
        contenido = data.get("contenido")
        categoria_id = data.get("categoria_id", 1)
        user_id = get_jwt_identity()
        if not titulo or not contenido:
            return jsonify({"msg":"faltan campos"}), 400
        p = post_service.create_post(titulo, contenido, user_id, categoria_id)
        return jsonify({"msg":"post creado","post_id": p.id}), 201

class PostDetailAPI(MethodView):
    def get(self, post_id):
        post = Post.query.get_or_404(post_id)
        return jsonify({
            "id": post.id,
            "titulo": post.titulo,
            "contenido": post.contenido,
            "usuario_id": post.usuario_id,
            "fecha_creacion": post.fecha_creacion.isoformat()
        }), 200

    @jwt_required()
    def put(self, post_id):
        post = Post.query.get_or_404(post_id)
        claims = get_jwt()
        user_repo = UserRepository()
        requester = user_repo.get_by_id(claims.get("user_id"))
        try:
            post_service.update_post(post, request.get_json() or {}, requester)
        except PermissionError:
            return jsonify({"msg":"No autorizado"}), 403
        return jsonify({"msg":"post actualizado"}), 200

    @jwt_required()
    def delete(self, post_id):
        post = Post.query.get_or_404(post_id)
        claims = get_jwt()
        user_repo = UserRepository()
        requester = user_repo.get_by_id(claims.get("user_id"))
        try:
            post_service.delete_post(post, requester)
        except PermissionError:
            return jsonify({"msg":"No autorizado"}), 403
        return jsonify({"msg":"post eliminado"}), 200

post_bp.add_url_rule("/posts", view_func=PostsAPI.as_view("posts_api"))
post_bp.add_url_rule("/posts/<int:post_id>", view_func=PostDetailAPI.as_view("post_detail_api"))
