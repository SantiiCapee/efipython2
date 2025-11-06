from models.models import Categoria, db

class CategoryRepository:
    @staticmethod
    def list_all():
        return Categoria.query.all()

    @staticmethod
    def create(nombre):
        c = Categoria(nombre=nombre)
        db.session.add(c)
        db.session.commit()
        return c

    @staticmethod
    def get_by_id(category_id):
        return Categoria.query.get(category_id)

    @staticmethod
    def update(cat):
        db.session.commit()
        return cat

    @staticmethod
    def delete(cat):
        db.session.delete(cat)
        db.session.commit()
