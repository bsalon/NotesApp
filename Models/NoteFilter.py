from Models.BaseModel import BaseModel

from datetime import datetime
from peewee import *


class NoteFilterModel(BaseModel):
    note_name = CharField(unique=True)
    note_min_priority = IntegerField()
    note_max_priority = IntegerField()
    note_min_time = DateTimeField(default=datetime.min)
    note_max_time = DateTimeField(default=datetime.now)
    note_text = TextField()
    tag_name = CharField(unique=True)
    tag_description = TextField()
    category_name = CharField(unique=True)
    category_description = TextField()
