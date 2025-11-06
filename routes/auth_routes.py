from flask import Blueprint, request, jsonify
from flask.views import MethodView
from services.auth_service import AuthService
from flask_jwt_extended import create_access_token

auth_bp = Blueprint("auth", __name__)
auth_service = AuthService()

class RegisterAPI(MethodView):
    def post(self):
        data = request.get_json() or {}
        nombre = data.get("nombre")
        email = data.get("email")
        password = data.get("password")
        if not nombre or not email or not password:
            return jsonify({"msg":"Faltan campos"}), 400
        try:
            user = auth_service.register(nombre, email, password)
        except ValueError as e:
            return jsonify({"msg": str(e)}), 400
        return jsonify({"message":"Usuario creado","user_id": user.id}), 201

class LoginAPI(MethodView):
    def post(self):
        data = request.get_json() or {}
        email = data.get("email")
        password = data.get("password")
        if not email or not password:
            return jsonify({"msg":"Faltan campos"}), 400
        user = auth_service.authenticate(email, password)
        if not user:
            return jsonify({"msg":"Credenciales inválidas"}), 401
        claims = {"user_id": user.id, "email": user.email, "role": user.role}
        token = create_access_token(identity=str(user.id), additional_claims=claims)
        return jsonify({"access_token": token}), 200

auth_bp.add_url_rule("/register", view_func=RegisterAPI.as_view("register_api"))
auth_bp.add_url_rule("/login", view_func=LoginAPI.as_view("login_api"))
