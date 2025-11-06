from flask import Blueprint, request, jsonify
from flask.views import MethodView
from services.category_service import CategoryService
from models.models import Categoria
from schemas.schemas import CategorySchema
from flask_jwt_extended import jwt_required
from decorators.roles_decorator import roles_required
from marshmallow import ValidationError

category_bp = Blueprint("category", __name__)
category_service = CategoryService()

class CategoryListAPI(MethodView):
    def get(self):
        cats = category_service.list_categories()
        return jsonify([{"id":c.id,"nombre":c.nombre} for c in cats]), 200

    @jwt_required()
    @roles_required("moderator", "admin")
    def post(self):
        schema = CategorySchema()
        try:
            data = schema.load(request.get_json(silent=True) or {})
        except ValidationError as e:
            return jsonify({"msg":"validation_error","errors": e.messages}), 400

        nombre = data["nombre"]
        c = category_service.create(nombre)
        return jsonify({"msg":"categoria creada","id":c.id}), 201

class CategoryDetailAPI(MethodView):
    @jwt_required()
    @roles_required("moderator", "admin")
    def put(self, category_id):
        cat = Categoria.query.get_or_404(category_id)
        schema = CategorySchema()
        try:
            data = schema.load(request.get_json(silent=True) or {})
        except ValidationError as e:
            return jsonify({"msg":"validation_error","errors": e.messages}), 400

        nombre = data["nombre"]
        category_service.update(cat, nombre)
        return jsonify({"msg":"categoria actualizada"}), 200

    @jwt_required()
    @roles_required("admin")
    def delete(self, category_id):
        cat = Categoria.query.get_or_404(category_id)
        category_service.delete(cat)
        return jsonify({"msg":"categoria eliminada"}), 200

category_bp.add_url_rule("/categories", view_func=CategoryListAPI.as_view("categories_api"))
category_bp.add_url_rule("/categories/<int:category_id>", view_func=CategoryDetailAPI.as_view("category_detail_api"))
