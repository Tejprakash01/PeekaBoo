import os
from appdirs import user_data_dir

APP_NAME = "Peekaboo"
APP_AUTHOR = "Tej"

def get_base_dir():
    base = user_data_dir(APP_NAME, APP_AUTHOR)
    os.makedirs(base, exist_ok=True)
    return base

def get_intruder_dir():
    path = os.path.join(get_base_dir(), "intruders")
    os.makedirs(path, exist_ok=True)
    return path

def get_faces_dir():
    path = os.path.join(get_base_dir(), "faces")
    os.makedirs(path, exist_ok=True)
    return path

def get_logs_dir():
    path = os.path.join(get_base_dir(), "logs")
    os.makedirs(path, exist_ok=True)
    return path
