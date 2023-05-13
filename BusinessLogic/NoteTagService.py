from BusinessLogic.BaseService import BaseService

from Models.Note import NoteModel
from Models.NoteTag import NoteTagModel
from Models.Tag import TagModel


class NoteTagService(BaseService):
    """
    NoteTag operations
    """

    def __init__(self):
        super().__init__(NoteTagModel)


    def get_note_tags_by_note(self, note):
        """
        Gets all NoteTag instances with specific note

        :param note: NoteTag note

        :return: All NoteTag instances with specific note
        """

        return NoteTagModel \
            .select(NoteTagModel) \
            .where(NoteTagModel.note == note)


    def get_note_tags_by_tag(self, tag):
        """
        Gets all NoteTag instances with specific tag

        :param tag: NoteTag tag

        :return: All NoteTag instances with specific tag
        """

        return NoteTagModel \
            .select(NoteTagModel) \
            .where(NoteTagModel.tag == tag)
