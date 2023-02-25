from Models.BaseModel import BaseModel

from Models.Category import CategoryModel

from datetime import datetime
from peewee import *


class NoteModel(BaseModel):
    name = CharField(unique=True)
    priority = IntegerField()
    time = DateTimeField(default=datetime.now) # TODO rename to date_time
    text = TextField()
    category = ForeignKeyField(CategoryModel)
