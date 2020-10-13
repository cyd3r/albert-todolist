# -*- coding: utf-8 -*-

"""A simple TODO list."""

from albertv0 import *
import time
import os
import sys
# enable local module import
# relative imports don't work for some reason
sys.path.append(os.path.dirname(__file__))

__iid__ = "PythonInterface/v0.1"
__prettyname__ = "TODO List"
__version__ = "0.1"
__trigger__ = "todo"
__author__ = "cyd3r"
__dependencies__ = []

todo_path = os.path.dirname(__file__) + "/todo.txt"

iconPath = iconLookup("menu-editor")
if not iconPath:
    iconPath = os.path.dirname(__file__) + "/todo.svg"

def add_entry(text):
    with open(todo_path) as todo_file:
        lines = todo_file.readlines()
    lines.append(text + "\n")
    with open(todo_path, "w") as todo_file:
        todo_file.writelines(lines)

def remove_entry(text):
    with open(todo_path) as todo_file:
        lines = todo_file.readlines()
    with open(todo_path, "w") as todo_file:
        for line in lines:
            if line.strip() != text:
                todo_file.write(line)

def initialize():
    # create file if it does not exist
    if not os.path.exists(todo_path):
        with open(todo_path, "w") as todo_file:
            pass

def handleQuery(query):
    if not query.isTriggered:
        return

    # avoid rate limiting
    time.sleep(0.1)
    if not query.isValid:
        return

    stripped = query.string.strip()

    items = []

    try:
        with open(todo_path) as todo_file:
            for line in todo_file.readlines():
                line = line.strip().lower()
                if line and (not stripped or stripped.lower() in line):
                    def create_callable(entry_name):
                        def func():
                            remove_entry(entry_name)
                        return FuncAction(text="Remove", callable=func)
                    item = Item(
                        id=__prettyname__,
                        icon=iconPath,
                        text=line,
                        subtext="Select and press enter to remove",
                        actions=[create_callable(line)],
                    )
                    items.append(item)
    except:
        pass

    if len(items) == 0 and stripped:
        items.append(Item(
            id=__prettyname__,
            icon=iconPath,
            text=stripped,
            subtext="Create new entry",
            actions=[FuncAction(text="Create new entry", callable=lambda: add_entry(stripped))],
        ))

    return items

