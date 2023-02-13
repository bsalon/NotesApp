from Models.BaseModel import BaseModel
from Models.Note import NoteModel

from peewee import *


class TagModel(BaseModel):
    note = ForeignKeyField(NoteModel, backref="tags")
    name = CharField(unique=True)
    description = TextField()
