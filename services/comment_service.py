from repositories.comment_repository import CommentRepository

class CommentService:
    def __init__(self):
        self.repo = CommentRepository()

    def list_comments(self, post_id):
        return self.repo.get_by_post(post_id)

    def create_comment(self, texto, usuario_id, post_id):
        return self.repo.create(texto, usuario_id, post_id)

    def delete_comment(self, comment, requester):
        if requester.role in ("admin","moderator") or comment.usuario_id == requester.id:
            return self.repo.delete(comment)
        raise PermissionError("No autorizado")
