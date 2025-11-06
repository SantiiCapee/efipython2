from models.models import Comentario, db

class CommentRepository:
    @staticmethod
    def get_by_post(post_id):
        return Comentario.query.filter_by(post_id=post_id, is_visible=True).all()

    @staticmethod
    def create(texto, usuario_id, post_id):
        c = Comentario(texto=texto, usuario_id=usuario_id, post_id=post_id)
        db.session.add(c)
        db.session.commit()
        return c

    @staticmethod
    def delete(comment):
        db.session.delete(comment)
        db.session.commit()
