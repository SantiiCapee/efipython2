from repositories.category_repository import CategoryRepository

class CategoryService:
    def __init__(self):
        self.repo = CategoryRepository()

    def list_categories(self):
        return self.repo.list_all()

    def create(self, nombre):
        return self.repo.create(nombre)

    def update(self, cat, nombre):
        cat.nombre = nombre
        return self.repo.update(cat)

    def delete(self, cat):
        return self.repo.delete(cat)
