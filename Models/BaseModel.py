from peewee import *


db = SqliteDatabase("notes_database.db")

class BaseModel(Model):
    class Meta:
        database = db
