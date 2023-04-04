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
db.close()

