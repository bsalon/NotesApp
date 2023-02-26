import os.path

from datetime import datetime, timedelta
from peewee import *

from Models.Note import NoteModel
from Models.NoteTag import NoteTagModel
from Models.Tag import TagModel
from Models.Category import CategoryModel
from Models.NoteFilter import NoteFilterModel


db = SqliteDatabase(os.path.abspath(os.path.dirname(__file__)) + "/notes_database.db")

db.connect()
db.create_tables([NoteModel, NoteTagModel, TagModel, CategoryModel, NoteFilterModel])

categories = [category for category in CategoryModel.select()]
if len(categories) < 1:
    print("Creating test data [categories]")
    for i in range(10):
        CategoryModel.create(
            name = "Category " + str(i),
            description = "Description of the category " + str(i)
        )
categories = [category for category in CategoryModel.select()]

notes = [note for note in NoteModel.select()]
if len(notes) < 1:
    print("Creating test data [notes]")
    for i in range(20):
        NoteModel.create(
            name = "Note " + str(i),
            priority = i,
            time = datetime.now() + timedelta(hours = i),
            text = "This is just some text for note " + str(i),
            category = categories[i // 5]
        )
notes = [note for note in NoteModel.select()]

tags = [tag for tag in TagModel.select()]
if len(tags) < 1:
    print("Creating test data [tags]")
    for i in range(10):
        TagModel.create(
            name = "Tag " + str(i),
            description = "This is a description for the tag " + str(i)
        )
tags = [tag for tag in TagModel.select()]

# FIXME
notes_tags = [note_tag for note_tag in NoteTagModel.select()]
if len(notes_tags) < 1:
    print("Creating test data [notes_tags]")
    for i in range(20):
        for j in range(3):
            NoteTagModel.create(
                note = notes[i // 2],
                tag = tags[(i % 8) + j]
            )

filters = [note_filter for note_filter in NoteFilterModel.select()]
if len(filters) < 1:
    print("Creating test data [fast filters]")
    for i in range(10):
        NoteFilterModel.create(
            name = "Filter " + str(i),
            note_name = "",
            note_min_priority = 0 + i,
            note_max_priority = 100 - i,
            note_min_time = datetime.min,
            note_max_time = datetime.now(),
            note_text = "",
            tag_name = "",
            tag_description = "",
            category_name = "",
            category_description = "",
            order = i
        )

db.close()

