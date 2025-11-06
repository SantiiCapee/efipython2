from flask import Blueprint, request, jsonify
from flask.views import MethodView
from services.auth_service import AuthService
from flask_jwt_extended import create_access_token
from schemas.schemas import UserRegisterSchema, LoginSchema
from marshmallow import ValidationError

auth_bp = Blueprint("auth", __name__)
auth_service = AuthService()

class RegisterAPI(MethodView):
    def post(self):
        raw = request.get_json(silent=True) or {}
        schema = UserRegisterSchema()
        try:
            data = schema.load(raw)
        except ValidationError as e:
            return jsonify({"msg":"validation_error","errors": e.messages}), 400

        nombre = data["nombre"]
        email = data["email"]
        password = data["password"]
        role = data.get("role", "user")

        try:
            user = auth_service.register(nombre, email, password)
            if role and hasattr(user, "role"):
                user.role = role
                from app import db
                db.session.commit()
        except ValueError as e:
            return jsonify({"msg": str(e)}), 400

        return jsonify({"message":"Usuario creado","user_id": user.id}), 201

class LoginAPI(MethodView):
    def post(self):
        raw = request.get_json(silent=True) or {}
        schema = LoginSchema()
        try:
            data = schema.load(raw)
        except ValidationError as e:
            return jsonify({"msg":"validation_error","errors": e.messages}), 400

        email = data["email"]
        password = data["password"]
        user = auth_service.authenticate(email, password)
        if not user:
            return jsonify({"msg":"Credenciales inválidas"}), 401

        claims = {"user_id": user.id, "email": user.email, "role": user.role}
        token = create_access_token(identity=str(user.id), additional_claims=claims)
        return jsonify({"access_token": token}), 200

auth_bp.add_url_rule("/register", view_func=RegisterAPI.as_view("register_api"))
auth_bp.add_url_rule("/login", view_func=LoginAPI.as_view("login_api"))
