from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost/db_efipython"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "super_secret_key"

db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

# importa modelos y vistas AFTER init de db/ma para evitar ciclos
from models import Usuario, UserCredential, Post, Comentario
from views import (
    UserAPI,
    UserDetailAPI,
    UserRegisterAPI,
    LoginAPI,
    PostsAPI,
    PostDetailAPI,
)

# RUTAS USUARIOS
app.add_url_rule("/users", view_func=UserAPI.as_view("user_api"), methods=["GET", "POST"])
app.add_url_rule("/users/<int:id>", view_func=UserDetailAPI.as_view("user_detail_api"), methods=["GET","PUT","PATCH","DELETE"])

# AUTH
app.add_url_rule("/register", view_func=UserRegisterAPI.as_view("register_api"), methods=["POST"])
app.add_url_rule("/login", view_func=LoginAPI.as_view("login_api"), methods=["POST"])

# POSTS (mínimo para que no rompa)
app.add_url_rule("/posts", view_func=PostsAPI.as_view("posts_api"), methods=["GET","POST"])
app.add_url_rule("/posts/<int:post_id>", view_func=PostDetailAPI.as_view("post_detail_api"), methods=["GET","PUT","DELETE"])

if __name__ == "__main__":
    app.run(debug=True)
