from repositories.post_repository import PostRepository
from repositories.user_repository import UserRepository

class PostService:
    def __init__(self):
        self.repo = PostRepository()

    def get_public_posts(self):
        return self.repo.get_all_published()

    def create_post(self, titulo, contenido, user_id, categoria_id):
        return self.repo.create(titulo, contenido, user_id, categoria_id)

    def update_post(self, post, data, requester):
        if requester.role != "admin" and post.usuario_id != requester.id:
            raise PermissionError("No autorizado")
        post.titulo = data.get("titulo", post.titulo)
        post.contenido = data.get("contenido", post.contenido)
        return self.repo.update(post)

    def delete_post(self, post, requester):
        if requester.role != "admin" and post.usuario_id != requester.id:
            raise PermissionError("No autorizado")
        return self.repo.delete(post)
