import os.path

from datetime import datetime, timedelta
from peewee import *

from Models.Note import NoteModel
from Models.Tag import TagModel
from Models.Category import CategoryModel
from Models.NoteFilter import NoteFilterModel


db = SqliteDatabase(os.path.abspath(os.path.dirname(__file__)) + "/notes_database.db")

db.connect()
db.create_tables([NoteModel, TagModel, CategoryModel, NoteFilterModel])

notes = [note for note in NoteModel.select()]
if len(notes) < 1:
    print("creating")
    for i in range(20):
        NoteModel.create(
            name = "note " + str(i),
            priority = i,
            time = datetime.now() + timedelta(hours = i),
            text = "This is just some text for note " + str(i)
        )

db.close()
