from models.models import Post, db

class PostRepository:
    @staticmethod
    def get_all_published():
        return Post.query.filter_by(is_published=True).all()

    @staticmethod
    def get_by_id(post_id):
        return Post.query.get(post_id)

    @staticmethod
    def create(titulo, contenido, usuario_id, categoria_id):
        post = Post(titulo=titulo, contenido=contenido, usuario_id=usuario_id, categoria_id=categoria_id)
        db.session.add(post)
        db.session.commit()
        return post

    @staticmethod
    def update(post):
        db.session.commit()
        return post

    @staticmethod
    def delete(post):
        db.session.delete(post)
        db.session.commit()
