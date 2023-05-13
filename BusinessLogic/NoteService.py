from peewee import JOIN

from BusinessLogic.BaseService import BaseService

from Models.Note import NoteModel
from Models.NoteTag import NoteTagModel
from Models.Tag import TagModel
from Models.Category import CategoryModel


class NoteService(BaseService):
    """
    Note operations
    """

    def __init__(self):
        super().__init__(NoteModel)


    def get_paged_filtered(self, filters, page, size):
        """
        Gets paginated and filtered notes

        :param filters: Filters to be applied on notes
        :param page: Pagination page
        :param size: Pagination size

        :return: Paginated and filtered notes
        """

        query = self._joined_note_query()
        filtered_query = self._filter_note_query(query, filters)
        return filtered_query.offset((page - 1) * size).limit(size).order_by(NoteModel.priority).group_by(NoteModel.name)


    def get_all_filtered(self, filters):
        """
        Gets filtered notes

        :param filters: Filters to be applied on notes

        :return: Filtered notes
        """

        query = self._joined_note_query()
        return self._filter_note_query(query, filters)


    def find_detailed_by_name(self, note_name):
        """
        Gets detailed information of note with specific name

        :param note_name: Note name

        :return: Detailed information of note with specific name
        """

        return self._joined_note_query() \
            .where(NoteModel.name == note_name)


    def update_note(self, note, updated_note):
        """
        Updates note with new note values

        :param note: Old note
        :param updated_note: New note values

        :return: Return value of the query
        """

        return NoteModel \
            .update(name = updated_note.name, \
                time = updated_note.time, \
                text = updated_note.text, \
                priority = updated_note.priority, \
                category = updated_note.category) \
            .where(NoteModel.id == note.id) \
            .execute()


    def exists_by_category(self, category):
        """
        Checks if note with category exists

        :param category: Note category

        :return: True if note with category exists False otherwise
        """

        return NoteModel \
            .select() \
            .where(NoteModel.category == category) \
            .exists()


    def exists_by_category_name(self, category_name):
        """
        Checks if note with category name exists

        :param category: Note category name

        :return: True if note with category name exists False otherwise
        """

        return NoteModel \
            .select() \
            .where(NoteModel.category.name == category_name) \
            .exists()


    def _joined_note_query(self):
        """
        Joins all note relationships

        :return: Detailed information about the note
        """

        return NoteModel \
            .select(NoteModel, CategoryModel, NoteTagModel, TagModel) \
            .join(CategoryModel, JOIN.LEFT_OUTER) \
            .switch(NoteModel) \
            .join(NoteTagModel, JOIN.LEFT_OUTER) \
            .join(TagModel, JOIN.LEFT_OUTER)


    def _filter_note_query(self, query, filters):
        """
        Gets filtered query

        :param query: Query to be filtered
        :param filters: Filters to be applied

        :return: Filtered query
        """

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
