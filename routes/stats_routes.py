from flask import Blueprint, jsonify
from flask.views import MethodView
from models.models import Post, Comentario, Usuario
from decorators.roles_decorator import roles_required
from flask_jwt_extended import jwt_required, get_jwt

stats_bp = Blueprint("stats", __name__)

class StatsAPI(MethodView):
    @jwt_required()
    @roles_required("moderator","admin")
    def get(self):
        total_posts = Post.query.count()
        total_comments = Comentario.query.count()
        total_users = Usuario.query.count()
        data = {
            "total_posts": total_posts,
            "total_comments": total_comments,
            "total_users": total_users
        }
        claims = get_jwt()
        if claims.get("role") == "admin":
            from datetime import datetime, timedelta
            since = datetime.utcnow() - timedelta(days=7)
            posts_last_week = Post.query.filter(Post.fecha_creacion >= since).count()
            data["posts_last_week"] = posts_last_week
        return jsonify(data), 200

stats_bp.add_url_rule("/stats", view_func=StatsAPI.as_view("stats_api"))
