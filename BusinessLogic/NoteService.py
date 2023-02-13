from BusinessLogic.BaseService import BaseService

from Models.Note import NoteModel


class CategoryService(BaseService):
    def __init__(self):
        super().__init__(NoteModel)
