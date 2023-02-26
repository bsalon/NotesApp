from Models.BaseModel import BaseModel

from datetime import datetime
from peewee import *


class NoteFilterModel(BaseModel):
    name = CharField(unique=True)
    note_name = CharField()
    note_min_priority = IntegerField(default=0)
    note_max_priority = IntegerField(default=100)
    note_min_time = DateTimeField(default=datetime.min)
    note_max_time = DateTimeField(default=datetime.now)
    note_text = TextField()
    tag_name = CharField()
    tag_description = TextField()
    category_name = CharField()
    category_description = TextField()
    order = IntegerField()
