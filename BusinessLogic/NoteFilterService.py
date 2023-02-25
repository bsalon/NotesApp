from BusinessLogic.BaseService import BaseService

from Models.NoteFilter import NoteFilterModel


class NoteFilterService(BaseService):
    def __init__(self):
        super().__init__(NoteFilterModel)

