from BusinessLogic.BaseService import BaseService

from Models.Note import NoteModel


class NoteService(BaseService):
    def __init__(self):
        super().__init__(NoteModel)


if __name__ == "__main__":
    service = NoteService()
    notes = [note for note in service.get_all()]
    # service.create(name="First note", priority=0, text="This is the first note")
    print(notes)
