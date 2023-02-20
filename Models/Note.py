from Models.BaseModel import BaseModel

from datetime import datetime
from peewee import *


class NoteModel(BaseModel):
    name = CharField(unique=True)
    priority = IntegerField()
    time = DateTimeField(default=datetime.now)
    text = TextField()
