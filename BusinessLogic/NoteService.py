from peewee import JOIN

from BusinessLogic.BaseService import BaseService

from Models.Note import NoteModel
from Models.NoteTag import NoteTagModel
from Models.Tag import TagModel
from Models.Category import CategoryModel


class NoteService(BaseService):
    def __init__(self):
        super().__init__(NoteModel)


    def get_paged_filtered(self, filters, page, size):
        query = self.get_all_filtered(filters)
        return query.offset((page - 1) * size).limit(size)


    def get_all_filtered(self, filters):
        query = NoteModel \
            .select(NoteModel, CategoryModel, NoteTagModel, TagModel) \
            .join(CategoryModel, JOIN.LEFT_OUTER) \
            .switch(NoteModel) \
            .join(NoteTagModel, JOIN.LEFT_OUTER) \
            .join(TagModel, JOIN.LEFT_OUTER) \
            .where(NoteModel.name.contains(filters.note_name)) \
            .where(NoteModel.priority >= filters.note_min_priority) \
            .where(NoteModel.priority <= filters.note_max_priority) \
            .where(NoteModel.time >= filters.note_min_time) \
            .where(NoteModel.time <= filters.note_max_time) \
            .where(NoteModel.text.contains(filters.note_text)) \
            .where(CategoryModel.name.contains(filters.category_name)) \
            .where(CategoryModel.description.contains(filters.category_description))
        
        # this would break the query when the note has no tags -- we need if statement
        if filters.tag_name or filters.tag_description:
            query = query.where(TagModel.name.contains(filters.tag_name)) \
                .where(TagModel.description.contains(filters.tag_description))
        
        #query = query.group_by(NoteModel, CategoryModel, NoteTagModel, TagModel)
        return query


    def find_detailed_by_name(self, note_name):
        return NoteModel \
            .select(NoteModel, CategoryModel, NoteTagModel, TagModel) \
            .join(CategoryModel, JOIN.LEFT_OUTER) \
            .switch(NoteModel) \
            .join(NoteTagModel, JOIN.LEFT_OUTER) \
            .join(TagModel, JOIN.LEFT_OUTER) \
            .where(NoteModel.name == note_name)


    def update_note(self, note, updated_note):
        return NoteModel \
            .update(name = updated_note.name, \
                time = updated_note.time, \
                text = updated_note.text, \
                priority = updated_note.priority, \
                category = updated_note.category) \
            .where(NoteModel.id == note.id) \
            .execute()


if __name__ == "__main__":
    service = NoteService()
    notes = [note for note in service.get_all()]
    print(notes)
