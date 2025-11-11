from marshmallow import Schema, fields, validate

class UserRegisterSchema(Schema):
    nombre = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)
    role = fields.Str(load_default="user", validate=validate.OneOf(["user","moderator","admin"]))

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    nombre = fields.Str(required=True)
    email = fields.Email(required=True)
    role = fields.Str(dump_default="user")
    is_active = fields.Bool(dump_default=True)
    created_at = fields.DateTime(dump_only=True)

class PostSchema(Schema):
    id = fields.Int(dump_only=True)
    titulo = fields.Str(required=True)
    contenido = fields.Str(required=True)
    usuario_id = fields.Int(dump_only=True)
    fecha_creacion = fields.DateTime(dump_only=True)
    author = fields.Method("get_author", dump_only=True)

    def get_author(self, post):
        return post.usuario.nombre if post.usuario else None


class ComentarioSchema(Schema):
    id = fields.Int(dump_only=True)
    texto = fields.Str(required=True)
    usuario_id = fields.Int(dump_only=True)
    post_id = fields.Int(required=True)
    fecha_creacion = fields.DateTime(dump_only=True)
    usuario = fields.Nested(UserSchema, only=("id", "nombre"))
    post = fields.Nested(PostSchema, only=("id", "titulo"))
