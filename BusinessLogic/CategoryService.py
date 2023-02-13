from BusinessLogic.BaseService import BaseService

from Models.Category import CategoryModel


class CategoryService(BaseService):
    def __init__(self, *args, **kwargs):
        super().__init__(CategoryModel, *args, **kwargs)
