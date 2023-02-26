from BusinessLogic.BaseService import BaseService

from Models.Note import NoteModel
from Models.NoteTag import NoteTagModel
from Models.Tag import TagModel


class NoteTagService(BaseService):
    def __init__(self):
        super().__init__(NoteTagModel)


    def get_note_tags_by_note(self, note):
        return NoteTagModel \
            .select(NoteTagModel) \
            .where(NoteTagModel.note == note)


    def get_note_tags_by_tag(self, tag):
        return NoteTagModel \
            .select(NoteTagModel) \
            .where(NoteTagModel.tag == tag)
