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
        query = self._joined_note_query()
        filtered_query = self._filter_note_query(query, filters)
        return filtered_query.offset((page - 1) * size).limit(size).order_by(NoteModel.priority).group_by(NoteModel.name)


    def get_all_filtered(self, filters):
        query = self._joined_note_query()
        return self._filter_note_query(query, filters)


    def find_detailed_by_name(self, note_name):
        return self._joined_note_query() \
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


    def exists_by_category(self, category): # FIXME
        return NoteModel \
            .select() \
            .where(NoteModel.category == category) \
            .exists()


    def exists_by_category_name(self, category_name): # FIXME
        return NoteModel \
            .select() \
            .where(NoteModel.category.name == category_name) \
            .exists()


    def _joined_note_query(self):
        return NoteModel \
            .select(NoteModel, CategoryModel, NoteTagModel, TagModel) \
            .join(CategoryModel, JOIN.LEFT_OUTER) \
            .switch(NoteModel) \
            .join(NoteTagModel, JOIN.LEFT_OUTER) \
            .join(TagModel, JOIN.LEFT_OUTER)


    def _filter_note_query(self, query, filters):
        if filters == None:
            return query
        
        query = query \
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
        
        return query



if __name__ == "__main__":
    service = NoteService()
    notes = [note for note in service.get_all()]
    print(notes)
