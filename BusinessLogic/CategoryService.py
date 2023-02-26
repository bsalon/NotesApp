from BusinessLogic.BaseService import BaseService

from Models.Category import CategoryModel


class CategoryService(BaseService):
    def __init__(self, *args, **kwargs):
        super().__init__(CategoryModel, *args, **kwargs)


    def update_category(self, category, updated_category):
        return CategoryModel \
            .update(name = updated_category.name, \
                description = updated_category.description) \
            .where(CategoryModel.id == category.id) \
            .execute()

