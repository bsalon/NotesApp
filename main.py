#!/usr/bin/env python3

import argparse

from PySideApp import main as PySideAppMain
from TkinterApp import main as TkinterAppMain

from Database import create_test_data


def create_app_parser():
    parser = argparse.ArgumentParser(description="Run notes application using specified library.")
    parser.add_argument("--create-data",
                        default=False, action="store_true",
                        help="if there is no data, create test data for the application")
    parser.add_argument("library",
                        nargs="?", default="PySide", action="store",
                        choices=["PySide", "Tkinter", "Kivy"],
                        help="the GUI library used in the application (default is PySide)")
    return parser


if __name__ == "__main__":
    parser = create_app_parser()
    
    args = parser.parse_args()
    if args.create_data:
        create_test_data.create_test_data()

    if args.library == "PySide":
        PySideAppMain.run_application()
    elif args.library == "Tkinter":
        TkinterAppMain.run_application()
    elif args.library == "Kivy":
        # This import style is needed, otherwise
        # Kivy would create a new empty window
        from KivyApp import main as KivyAppMain
        KivyAppMain.run_application()
    else:
        print(f"Invalid library {args.library}")
