# import View
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


    def create_note(self, **keys_values):
        self.note_service.create(**key_values)
    

    def get_notes(self):
        return [note for note in self.note_service.get_all()]


    def get_filtered_notes_paged(self, filters, page, size):
        return [note for note in self.note_service.get_paged_filtered(filters, page, size)]


    def get_filtered_notes(self, filters):
        # note.category.name ... note.notetagmode.note.name
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
        #if self.note_service.get_by_name(updated_note.name):
        #    return None

        note_tags = self.notetag_service.get_note_tags(note)
        for note_tag in note_tags:
            note_tag.delete_instance()

        updated_note.category = self.category_service.get_by_name(note.category.name)
        query_result = self.note_service.update_note(note, updated_note)

        for tag_name in updated_note.tags_names:
            found_tag = self.tag_service.get_by_name(tag_name)
            self.notetag_service.create(note=new_note, tag=found_tag)

        print(query_result)

        return query_result


    def delete_notes(self, notes_names): # FIXME: delete tags and categories
        notes = []
        for note_name in notes_names:
            note = self.note_service.get_by_name(note_name)
            note.delete_instance()



    # TODO add here
    def create_category(self, **keys_values):
        self.category_service.create(**key_values)


    def get_categories(self):
        return [category for category in self.category_service.get_all()]


    def delete_categories(self, notes_names): # FIXME: dont delete if note exists
        categories = []



    # TODO add here
    def create_tag(self, **keys_values):
        self.tag_service.create(**key_values)


    def get_tags(self):
        return [tag for tag in self.tag_service.get_all()]


    def delete_tags(self, tags_names): # FIXME: dont delete if note exists
        tags = []



    # TODO add here
    def create_filter(self, **keys_values):
        self.filter_service.create(**key_values)


    def get_filters(self):
        return [fast_filter for fast_filter in self.filter_service.get_all()]
    

    def find_filter_by_name(self, note_name): # TODO
        return self.filter_service.get_by_name(note_name)


    def delete_filters(self, filters_names):
        filters = []


