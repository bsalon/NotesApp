from Models.BaseModel import BaseModel

from peewee import *


class CategoryModel(BaseModel):
    name = CharField(unique=True)
    description = TextField()
