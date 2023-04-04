# NotesApp

This application is part of my diploma thesis at the Faculty of Informatics of Masaryk University. It compares three different Python GUI libraries. The applications are meant to be implemented as close as possible. In some cases, applications differ because of a lack of support for a specific element or the complexity of implementing a particular feature. Dialog windows are created with more significant differences to demonstrate the specifics and defaults of individual libraries.

Used libraries are:
```
PySide6
Tkinter
Kivy
```

## Install

Before running the application, you will need to have these packages installed:
```
Kivy
kivymd
peewee
PySide6
tkcalendar
```

You can install these packages using the pip command:
``` console
$ pip3 install Kivy kivymd peewee PySide6 tkcalendar
```

If you want to use versions used in the development, run:
``` console
$ pip3 install --requirement=requirements.txt
```

## Run

You can run the application using the *main.py* file:
``` console
$ python3.10 main.py -h
usage: main.py [-h] [--create-data] [{PySide,Tkinter,Kivy}]

Run notes application using specified library.

positional arguments:
  {PySide,Tkinter,Kivy}
                        the GUI library used in the application (default is PySide)

options:
  -h, --help            show this help message and exit
  --create-data         if there is no data, create test data for the application
```

You can also run the application using individual libraries running the *main.py* file of a specific subproject, i.e.:
``` console
$ cd TkinterApp
$ python3.10 main.py
```
