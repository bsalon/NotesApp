from BusinessLogic.BaseService import BaseService

from Models.NoteFilter import NoteFilterModel


class NoteFilterService(BaseService):
    """
    Filter operations
    """

    def __init__(self):
        super().__init__(NoteFilterModel)


    def find_by_order(self, order):
        """
        Finds all NoteFilter instances with specific order

        :param order: NoteFilter order

        :return: All NoteFilter instances with specific order
        """

        return NoteFilterModel.select().where(NoteFilterModel.order == order)


    def update_filter(self, note_filter, updated_filter):
        """
        Updates NoteFilter with new NoteFilter values

        :param note_filter: Old NoteFilter
        :param updated_filter: New NoteFilter values

        :return: Return value of the query
        """

        return NoteFilterModel \
            .update(name = updated_filter.name, \
                note_name = updated_filter.note_name, \
                note_min_priority = updated_filter.note_min_priority, \
                note_max_priority = updated_filter.note_max_priority, \
                note_min_time = updated_filter.note_min_time, \
                note_max_time = updated_filter.note_max_time, \
                note_text = updated_filter.note_text, \
                tag_name = updated_filter.tag_name, \
                tag_description = updated_filter.tag_description, \
                category_name = updated_filter.category_name, \
                category_description = updated_filter.category_description, \
                order = updated_filter.order) \
            .where(NoteFilterModel.id == note_filter.id) \
            .execute()


    def remove_order(self, order):
        """
        Deletes all NoteFilter instances with specific order

        :param order: NoteFilter order

        :return: Return value of the query
        """

        return NoteFilterModel \
            .update(order = -1) \
            .where(NoteFilterModel.order == order) \
            .execute()
        
