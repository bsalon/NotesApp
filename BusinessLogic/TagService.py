from BusinessLogic.BaseService import BaseService

from Models.Tag import TagModel


class TagService(BaseService):
    def __init__(self):
        super().__init__(TagModel)
