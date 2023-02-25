from Models.BaseModel import BaseModel
from Models.Note import NoteModel
from Models.Tag import TagModel

from peewee import *


class NoteTagModel(BaseModel):
    note = ForeignKeyField(NoteModel)
    tag = ForeignKeyField(TagModel)
