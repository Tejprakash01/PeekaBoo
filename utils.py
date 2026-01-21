import os
import subprocess
import sys
from storage import get_faces_dir, get_intruder_dir


def open_faces_folder():
    folder = get_faces_dir()
    os.makedirs(folder, exist_ok=True)
    open_folder(folder)


def open_intruder_folder():
    folder = get_intruder_dir()
    os.makedirs(folder, exist_ok=True)
    open_folder(folder)


def open_folder(path):
    try:
        if sys.platform.startswith("win"):
            os.startfile(path)
        elif sys.platform.startswith("darwin"):
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])
    except Exception as e:
        print("Failed to open folder:", e)
