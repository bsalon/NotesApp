from Models.BaseModel import BaseModel
from Models.Note import NoteModel

from peewee import *


class TagModel(BaseModel):
    name = CharField(unique=True)
    description = TextField()
