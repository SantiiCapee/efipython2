from flask import Blueprint, request, jsonify
from flask.views import MethodView
from repositories.user_repository import UserRepository
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from decorators.roles_decorator import roles_required

user_bp = Blueprint("user", __name__)
user_repo = UserRepository()

class UsersAPI(MethodView):
    @jwt_required()
    @roles_required("admin")
    def get(self):
        users = user_repo.list_all()
        return jsonify([{"id":u.id,"nombre":u.nombre,"email":u.email,"role":u.role,"is_active":u.is_active} for u in users]), 200

class UserDetailAPI(MethodView):
    @jwt_required()
    def get(self, user_id):
        current = get_jwt_identity()
        claims = get_jwt()
        if current != user_id and claims.get("role") != "admin":
            return jsonify({"msg":"no autorizado"}), 403
        u = user_repo.get_by_id(user_id)
        return jsonify({"id":u.id,"nombre":u.nombre,"email":u.email,"role":u.role,"is_active":u.is_active}), 200

    @jwt_required()
    @roles_required("admin")
    def patch(self, user_id):
        data = request.get_json() or {}
        new_role = data.get("role")
        if new_role not in ("user","moderator","admin"):
            return jsonify({"msg":"role inválido"}), 400
        user_repo.update_role(user_id, new_role)
        return jsonify({"msg":"role actualizado"}), 200

    @jwt_required()
    @roles_required("admin")
    def delete(self, user_id):
        user_repo.deactivate(user_id)
        return jsonify({"msg":"usuario desactivado"}), 200

user_bp.add_url_rule("/users", view_func=UsersAPI.as_view("users_api"))
user_bp.add_url_rule("/users/<int:user_id>", view_func=UserDetailAPI.as_view("user_detail_api"))
user_bp.add_url_rule("/users/<int:user_id>/role", view_func=UserDetailAPI.as_view("user_role_api"), methods=["PATCH"])
