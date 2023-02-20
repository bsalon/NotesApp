# import View
from BusinessLogic.NoteService import NoteService


class NoteController():
    def __init__(self, *args, **kwargs):
        self.note_service = NoteService()
        self.view = None


    def create_note(self, **keys_values):
        pass
    

    def get_notes(self):
        notes = [note for note in self.note_service.get_all()]
        return notes
        # return self.view.notes_index(notes)


    def get_notes_detailed(self, page, size):
        pass
        # notes = [note for note in self.note_service.paginate()]


    def update_note(self):
        pass


    def delete_notes(self):
        pass



if __name__ == "__main__":
    controller = NoteController()
    notes = [note for note in controller.get_notes()]
    print(notes)
