from BusinessLogic.BaseService import BaseService

from Models.NoteFilter import NoteFilterModel


class CategoryService(BaseService):
    def __init__(self):
        super().__init__(NoteFilterModel)
