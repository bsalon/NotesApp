from Models.BaseModel import BaseModel
from Models.Note import NoteModel

from peewee import *


class CategoryModel(BaseModel):
    note = ForeignKeyField(NoteModel, backref="categories")
    name = CharField(unique=True)
    description = TextField()
