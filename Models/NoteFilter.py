from Models.BaseModel import BaseModel

from datetime import datetime
from peewee import *


class NoteFilter(BaseModel):
    note_name = CharField(unique=True)
    note_time = DateTimeField(default=datetime.now)
    note_text = TextField()
    tag_name = CharField(unique=True)
    tag_description = TextField()
    category_name = CharField(unique=True)
    category_description = TextField()
