from peewee import *

import os.path


class BaseModel(Model):
    class Meta:
        database = SqliteDatabase(os.path.abspath(os.path.dirname(__file__) + "/../Database") + "/notes_database.db")
