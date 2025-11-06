# 🧠 Proyecto EFI Python - API Flask (Blogcito)

Este proyecto es una **API REST** desarrollada con **Flask** para gestionar usuarios, posts, categorías y comentarios.  
Implementa **autenticación JWT**, **validación con Marshmallow**, y **ORM SQLAlchemy**.

---

## 🚀 Requisitos previos

Antes de ejecutar la aplicación, asegurate de tener instalado:

- Python 3.10 o superior  
- MySQL  
- pip (administrador de paquetes de Python)  
- Entorno virtual (opcional pero recomendado)

---

## ⚙️ Instalación y configuración

### 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/SantiiCapee/efipython2.git
cd efipython2
```

### 2️⃣ Crear entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # En Linux / Mac
venv\Scripts\activate     # En Windows
```

### 3️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4️⃣ Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto con este contenido:

```
SQLALCHEMY_DATABASE_URI=mysql+pymysql://root:@localhost/db_blogcito
SECRET_KEY=test123
JWT_SECRET_KEY=test123
FLASK_ENV=development
```

> 🔸 Ajustá el usuario, contraseña y nombre de base de datos según tu entorno MySQL.

---

## 🧩 Migraciones de base de datos

Si la base de datos no existe, creala en MySQL:

```sql
CREATE DATABASE db_blogcito;
```

Luego, dentro del entorno virtual:

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

---

## ▶️ Ejecución de la API

```bash
flask run
```

La API se ejecutará en:

```
http://127.0.0.1:5000/
```

---

## 🔐 Autenticación

Esta API utiliza **JWT (JSON Web Token)**.  
Debés **loguearte** primero para obtener un token y usarlo en las demás rutas protegidas.

### Login (`POST /api/login`)
```json
{
  "email": "admin@admin.com",
  "password": "admin"
}
```

Respuesta:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI..."
}
```

Luego, usá ese token en el header de cada petición protegida:
```
Authorization: Bearer <token>
```

---

## 🧭 Endpoints principales

### 🔸 Autenticación
| Método | Endpoint | Descripción |
|--------|-----------|-------------|
| POST | `/api/register` | Registro de usuario |
| POST | `/api/login` | Login (devuelve token JWT) |

### 🔸 Usuarios
| Método | Endpoint | Descripción |
|--------|-----------|-------------|
| GET | `/api/users` | Listar todos los usuarios *(solo admin)* |
| GET | `/api/users/<id>` | Obtener un usuario específico |
| PATCH | `/api/users/<id>` | Modificar usuario |
| DELETE | `/api/users/<id>` | Eliminar usuario |

### 🔸 Roles
| Método | Endpoint | Descripción |
|--------|-----------|-------------|
| PATCH | `/api/users/<id>/role` | Cambiar rol *(solo admin)* |

### 🔸 Categorías
| Método | Endpoint | Descripción |
|--------|-----------|-------------|
| GET | `/api/categories` | Listar categorías |
| POST | `/api/categories` | Crear categoría *(admin)* |
| PUT | `/api/categories/<id>` | Editar categoría |
| DELETE | `/api/categories/<id>` | Eliminar categoría |

### 🔸 Posts
| Método | Endpoint | Descripción |
|--------|-----------|-------------|
| GET | `/api/posts` | Listar posts |
| POST | `/api/posts` | Crear post |
| GET | `/api/posts/<id>` | Ver detalle del post |
| PUT | `/api/posts/<id>` | Editar post |
| DELETE | `/api/posts/<id>` | Eliminar post |

### 🔸 Comentarios
| Método | Endpoint | Descripción |
|--------|-----------|-------------|
| GET | `/api/posts/<id>/comments` | Listar comentarios de un post |
| POST | `/api/posts/<id>/comments` | Crear comentario |
| DELETE | `/api/comments/<id>` | Eliminar comentario |

### 🔸 Estadísticas
| Método | Endpoint | Descripción |
|--------|-----------|-------------|
| GET | `/api/stats` | Obtener estadísticas de la aplicación |

---

## 🧪 Pruebas con Thunder Client / Postman

1. Registrar un nuevo usuario (`POST /api/register`)  
2. Loguearse (`POST /api/login`) y copiar el token JWT  
3. En las peticiones siguientes, agregar el header:
   ```
   Authorization: Bearer <tu_token>
   ```
4. Probar los endpoints protegidos (crear post, comentarios, etc.)

---

## 👨‍💻 Roles disponibles

- **Administrador**: Puede crear, modificar y eliminar usuarios, categorías y posts.  
- **Usuario normal**: Puede crear posts y comentarios, pero no administrar otros usuarios.

---

## 🧱 Estructura del proyecto

```
efipython2/
│
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── schemas.py
│   ├── repositories.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── user.py
│   │   ├── post.py
│   │   ├── comment.py
│   │   ├── category.py
│   │   └── stats.py
│   └── utils/
│
├── migrations/
├── .env
├── requirements.txt
├── run.py
└── README.md
```

---

## 📚 Dependencias principales

- Flask  
- Flask-SQLAlchemy  
- Flask-Migrate  
- Flask-JWT-Extended  
- Marshmallow  
- PyMySQL  

---

## 💬 Autor

**Santiago Capellino**  
Proyecto EFI - Programación Avanzada en Python

---

## 🏁 Estado del proyecto

✅ API funcional con autenticación JWT, validación con Marshmallow, y endpoints completos para usuarios, categorías, posts, comentarios y estadísticas.
