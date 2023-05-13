#!/usr/bin/env python3

import argparse

from PySideApp import main as PySideAppMain
from TkinterApp import main as TkinterAppMain

from Database import create_test_data


def create_app_parser():
    """
    Creates argument parser

    :return: Argument parser
    """

    parser = argparse.ArgumentParser(description="Run notes application using specified library.")
    parser.add_argument("--create-data",
                        default=False, action="store_true",
                        help="if there is no data, create test data for the application")
    parser.add_argument("library",
                        nargs="?", default="PySide", action="store",
                        choices=["PySide", "Tkinter", "Kivy"],
                        help="the GUI library used in the application (default is PySide)")
    return parser


def run_application(library):
    """
    Runs the application using specified gui library

    :return: New gui library number
    """

    if library == "PySide":
        return PySideAppMain.run_application()
    elif library == "Tkinter":
        return TkinterAppMain.run_application()
    elif library == "Kivy":
        # This import style is needed, otherwise
        # Kivy would create a new empty window
        from KivyApp import main as KivyAppMain
        return KivyAppMain.run_application()
    else:
        print(f"Invalid library {library}")
    return -1


def library_from_number(gui_number):
    """
    Gets gui library name from gui library number

    :param gui_number: Gui library number

    :return: Gui library name
    """

    if gui_number == 0:
        return "PySide"
    elif gui_number == 1:
        return "Tkinter"
    elif gui_number == 2:
        return "Kivy"
    else:
        print(f"Invalid library number {gui_number}")
    return ""



if __name__ == "__main__":
    parser = create_app_parser()
    
    args = parser.parse_args()
    if args.create_data:
        create_test_data.create_test_data()

    library = args.library
    while True:
        gui_number = run_application(library)

        new_library = library_from_number(gui_number)
        if library == new_library:
            break
        library = new_library

