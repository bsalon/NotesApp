from peewee import *

import pathlib


class BaseModel(Model):
    class Meta:
        db_path = pathlib.Path(__file__).parent.parent / "Database" / "notes_database.db"
        database = SqliteDatabase(db_path.resolve().as_posix())
