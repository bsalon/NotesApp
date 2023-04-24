import os.path

from datetime import datetime, timedelta
from peewee import *

from Models.Note import NoteModel
from Models.NoteTag import NoteTagModel
from Models.Tag import TagModel
from Models.Category import CategoryModel
from Models.NoteFilter import NoteFilterModel


def create_test_data():
    db = SqliteDatabase(os.path.abspath(os.path.dirname(__file__)) + "/notes_database.db")
    db.connect()
    db.create_tables([NoteModel, NoteTagModel, TagModel, CategoryModel, NoteFilterModel])

    _create_categories()
    categories = [category for category in CategoryModel.select()]

    _create_notes(categories)
    _create_tags()
    notes = [note for note in NoteModel.select()]
    tags = [tag for tag in TagModel.select()]

    _create_notes_tags(notes, tags)
    _create_filters()

    db.close()



def _create_categories():
    categories = [category for category in CategoryModel.select()]

    if len([category.name for category in categories if category.name == "Default"]) == 0:
        CategoryModel.create(
            name = "Default",
            description = "Default category which can not be edited or deleted"
        )

    if len(categories) < 1:
        print("Creating test data [categories]")
        for i in range(10):
            CategoryModel.create(
                name = "Category " + str(i),
                description = "Description of the category " + str(i)
            )


def _create_notes(categories):
    notes = [note for note in NoteModel.select()]
    if len(notes) < 1:
        print("Creating test data [notes]")
        for i in range(20):
            NoteModel.create(
                name = "Note " + str(i),
                priority = i,
                time = datetime.now() + timedelta(hours = i),
                text = "This is just some text for note " + str(i),
                category = categories[(i // 5) // len(categories)]
            )


def _create_tags():
    tags = [tag for tag in TagModel.select()]
    if len(tags) < 1:
        print("Creating test data [tags]")
        for i in range(10):
            TagModel.create(
                name = "Tag " + str(i),
                description = "This is a description for the tag " + str(i)
            )


def _create_notes_tags(notes, tags):
    notes_tags = [note_tag for note_tag in NoteTagModel.select()]
    if len(notes_tags) < 1:
        print("Creating test data [notes_tags]")
        for i in range(20):
            for j in range(3):
                NoteTagModel.create(
                    note = notes[(i // 2) // len(notes)],
                    tag = tags[((i % 8) + j) // len(tags)]
                )


def _create_filters():
    filters = [note_filter for note_filter in NoteFilterModel.select()]
    if len(filters) < 1:
        print("Creating test data [fast filters]")
        for i in range(10):
            NoteFilterModel.create(
                name = "Filter " + str(i),
                note_name = str(i) if i % 2 == 0 else "",
                note_min_priority = 0 + i,
                note_max_priority = 100 - i,
                note_min_time = datetime.min,
                note_max_time = datetime.now(),
                note_text = "",
                tag_name = "",
                tag_description = "",
                category_name = str(i) if i % 3 == 0 else "",
                category_description = "",
                order = i
            )

