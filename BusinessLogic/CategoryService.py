from BusinessLogic.BaseService import BaseService

from Models.Category import CategoryModel


class CategoryService(BaseService):
    """
    Category operations
    """

    def __init__(self, *args, **kwargs):
        super().__init__(CategoryModel, *args, **kwargs)


    def update_category(self, category, updated_category):
        """
        Updates category with new category values

        :param category: Old category
        :param updated_category: New category values

        :return: Return value of the query
        """

        return CategoryModel \
            .update(name = updated_category.name, \
                description = updated_category.description) \
            .where(CategoryModel.id == category.id) \
            .execute()

