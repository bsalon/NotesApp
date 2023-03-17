from BusinessLogic.NoteService import NoteService
from BusinessLogic.NoteTagService import NoteTagService
from BusinessLogic.TagService import TagService
from BusinessLogic.CategoryService import CategoryService
from BusinessLogic.NoteFilterService import NoteFilterService


class UseCases():
    def __init__(self, *args, **kwargs):
        self.note_service = NoteService()
        self.notetag_service = NoteTagService()
        self.tag_service = TagService()
        self.category_service = CategoryService()
        self.filter_service = NoteFilterService()


    def create_note(self, note):
        if self.note_service.exists_by_name(note.name):
            return 0

        category = self.category_service.get_by_name(note.category_name)
        query_result = self.note_service.create(
            name=note.name,
            time=note.time,
            priority=note.priority,
            text=note.text,
            category=category
        )

        new_note = self.note_service.get_by_name(note.name)
        for tag_name in note.tags_names:
            tag = self.tag_service.get_by_name(tag_name)
            self.notetag_service.create(
                note=new_note,
                tag=tag
            )

        return query_result


    def get_notes(self):
        return [note for note in self.note_service.get_all()]


    def get_filtered_notes_paged(self, filters, page, size):
        notes = [note for note in self.note_service.get_paged_filtered(filters, page, size)]

        notes_with_tags = []
        for note in notes:
            notes_with_tags.append(note)
            notes_with_tags[-1].tags = set([notetag.tag.name for notetag in self.notetag_service.get_note_tags_by_note(note)])

        return notes_with_tags


    def get_filtered_notes(self, filters):
        return [note for note in self.note_service.get_all_filtered(filters)]

    
    def find_detailed_note_by_name(self, note_name):
        note_and_tags = [note_tag for note_tag in self.note_service.find_detailed_by_name(note_name)]

        note_with_tags = note_and_tags[0]
        note_with_tags.tags = set()
        for note_and_tag in note_and_tags:
            if note_and_tag.notetagmodel_set:
                note_with_tags.tags.add(note_and_tag.notetagmodel.tag.name)
        
        return note_with_tags


    def update_note(self, note_id, updated_note):
        note = self.note_service.get_by_id(note_id)
        if self.note_service.exists_by_name(updated_note.name) and note.name != updated_note.name:
            return 0

        note_tags = self.notetag_service.get_note_tags_by_note(note)
        for note_tag in note_tags:
            note_tag.delete_instance()

        updated_note.category = self.category_service.get_by_name(note.category.name)
        query_result = self.note_service.update_note(note, updated_note)
        new_note = self.note_service.get_by_id(note_id)

        for tag_name in updated_note.tags_names:
            found_tag = self.tag_service.get_by_name(tag_name)
            self.notetag_service.create(note=new_note, tag=found_tag)

        return query_result


    def delete_notes(self, notes_names):
        for note_name in notes_names:
            note = self.note_service.get_by_name(note_name)
            note_tags = self.notetag_service.get_note_tags_by_note(note)
            for note_tag in note_tags:
                note_tag.delete_instance()
            note.delete_instance()



    def create_category(self, category):
        if self.category_service.exists_by_name(category.name):
            return 0

        query_result = self.category_service.create(
            name=category.name,
            description=category.description
        )
        return query_result


    def get_categories(self):
        return [category for category in self.category_service.get_all()]


    def update_category(self, category_id, updated_category):
        category = self.category_service.get_by_id(category_id)
        if self.category_service.exists_by_name(updated_category.name) and category.name != updated_category.name:
            return 0

        query_result = self.category_service.update_category(category, updated_category)
        return query_result


    def find_category_by_name(self, category_name):
        return self.category_service.get_by_name(category_name)


    def find_categories_by_name(self, category_name):
        return [category for category in self.category_service.find_all_by_name(category_name)]


    def delete_categories(self, categories_names):
        categories = []
        for category_name in categories_names:
            category = self.category_service.get_by_name(category_name)
            if self.note_service.exists_by_category(category):
                return 0
            categories.append(category)

        for category in categories:
            category.delete_instance()

        return 1



    def create_tag(self, tag):
        if self.tag_service.exists_by_name(tag.name):
            return 0

        query_result = self.tag_service.create(
            name=tag.name,
            description=tag.description
        )
        return query_result


    def get_tags(self):
        return [tag for tag in self.tag_service.get_all()]


    def update_tag(self, tag_id, updated_tag):
        tag = self.tag_service.get_by_id(tag_id)
        if self.tag_service.exists_by_name(updated_tag.name) and tag.name != updated_tag.name:
            return 0

        query_result = self.tag_service.update_tag(tag, updated_tag)
        return query_result


    def find_tag_by_name(self, tag_name):
        return self.tag_service.get_by_name(tag_name)


    def find_tags_by_name(self, tag_name):
        return [tag for tag in self.tag_service.find_all_by_name(tag_name)]


    def delete_tags(self, tags_names):
        for tag_name in tags_names:
            tag = self.tag_service.get_by_name(tag_name)
            note_tags = self.notetag_service.get_note_tags_by_tag(tag)
            for note_tag in note_tags:
                note_tag.delete_instance()
            tag.delete_instance()



    def create_filter(self, note_filter):
        if self.filter_service.exists_by_name(note_filter.name):
            return 0

        self.filter_service.remove_order(note_filter.order)
        query_result = self.filter_service.create(
            name=note_filter.name,
            note_name=note_filter.note_name,
            note_min_priority=note_filter.note_min_priority,
            note_max_priority=note_filter.note_max_priority,
            note_min_time=note_filter.note_min_time,
            note_max_time=note_filter.note_max_time,
            note_text=note_filter.note_text,
            tag_name=note_filter.tag_name,
            tag_description=note_filter.tag_description,
            category_name=note_filter.category_name,
            category_description=note_filter.category_description,
            order=note_filter.order,
        )
        return query_result


    def get_filters(self):
        return [fast_filter for fast_filter in self.filter_service.get_all()]
    

    def update_filter(self, filter_id, updated_filter):
        note_filter = self.filter_service.get_by_id(filter_id)
        if self.filter_service.exists_by_name(updated_filter.name) and note_filter.name != updated_filter.name:
            return 0

        self.filter_service.remove_order(updated_filter.order)
        query_result = self.filter_service.update_filter(note_filter, updated_filter)
        return query_result


    def find_filter_by_name(self, note_name):
        return self.filter_service.get_by_name(note_name)


    def find_filters_by_name(self, name):
        return [fast_filter for fast_filter in self.filter_service.find_all_by_name(name)]


    def find_filter_by_order(self, order):
        query = self.filter_service.find_by_order(order)
        return query.get() if query.exists() else None


    def find_filter_by_order_listed(self, order):
        return [order_filter for order_filter in self.filter_service.find_by_order(order)]


    def delete_filters(self, filters_names):
        for filter_name in filters_names:
            fast_filter = self.filter_service.get_by_name(filter_name)
            fast_filter.delete_instance()

