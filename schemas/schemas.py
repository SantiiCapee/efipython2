from marshmallow import Schema, fields, validate, ValidationError, post_load

class UserRegisterSchema(Schema):
    username = fields.Str(load_default=None)
    nombre = fields.Str(load_default=None)
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))
    role = fields.Str(load_default="user", validate=validate.OneOf(["user","moderator","admin"]))

    @post_load
    def normalize(self, data, **kwargs):
        if data.get("username"):
            data["nombre"] = data.pop("username")
        if not data.get("nombre"):
            raise ValidationError({"nombre": ["Se requiere 'username' o 'nombre'."]})
        return data

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)

class PostSchema(Schema):
    titulo = fields.Str(required=True, validate=validate.Length(min=1))
    contenido = fields.Str(required=True, validate=validate.Length(min=1))
    categoria_id = fields.Int(required=True)

class PostUpdateSchema(Schema):
    titulo = fields.Str(validate=validate.Length(min=1))
    contenido = fields.Str(validate=validate.Length(min=1))
    is_published = fields.Boolean()

class CommentSchema(Schema):
    texto = fields.Str(required=True, validate=validate.Length(min=1))

class CategorySchema(Schema):
    nombre = fields.Str(required=True, validate=validate.Length(min=1))

class RolePatchSchema(Schema):
    role = fields.Str(required=True, validate=validate.OneOf(["user","moderator","admin"]))
