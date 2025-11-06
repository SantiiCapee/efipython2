from flask import Blueprint, request, jsonify
from flask.views import MethodView
from services.comment_service import CommentService
from models.models import Comentario, Post
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from repositories.user_repository import UserRepository

comment_bp = Blueprint("comment", __name__)
comment_service = CommentService()

class PostCommentsAPI(MethodView):
    def get(self, post_id):
        Post.query.get_or_404(post_id)
        comments = comment_service.list_comments(post_id)
        return jsonify([{"id":c.id,"texto":c.texto,"usuario_id":c.usuario_id,"fecha":c.fecha_creacion.isoformat()} for c in comments]), 200

    @jwt_required()
    def post(self, post_id):
        Post.query.get_or_404(post_id)
        data = request.get_json() or {}
        texto = data.get("texto")
        if not texto:
            return jsonify({"msg":"texto requerido"}), 400
        c = comment_service.create_comment(texto, get_jwt_identity(), post_id)
        return jsonify({"msg":"comentario creado","id": c.id}), 201

class CommentDeleteAPI(MethodView):
    @jwt_required()
    def delete(self, comment_id):
        comment = Comentario.query.get_or_404(comment_id)
        claims = get_jwt()
        requester = UserRepository.get_by_id(claims.get("user_id"))
        try:
            comment_service.delete_comment(comment, requester)
        except PermissionError:
            return jsonify({"msg":"no autorizado"}), 403
        return jsonify({"msg":"comentario eliminado"}), 200

comment_bp.add_url_rule("/posts/<int:post_id>/comments", view_func=PostCommentsAPI.as_view("post_comments_api"))
comment_bp.add_url_rule("/comments/<int:comment_id>", view_func=CommentDeleteAPI.as_view("comment_delete_api"))
