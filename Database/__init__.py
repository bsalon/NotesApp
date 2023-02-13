from ..Models import Note, Tag, Category, NoteFilter

db = SqliteDatabase("notes_database.db")

db.connect()
db.create_tables([Note, Tag, Category, NoteFilter])
