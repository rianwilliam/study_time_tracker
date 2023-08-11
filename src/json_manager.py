"""
Creates and manipulates the JSON file where it 
contains the text file directory with the saved time
"""
import os
import json
from typing import List

JSON_DIR = os.path.expanduser("~")  # Get the user's home directory
JSON_NAME = "study_data.json"
JSON_PATH = os.path.join(JSON_DIR, JSON_NAME)

TIME_FILE_NAME = "study_time"
DEFAULT_TIME_DIR = os.path.expanduser("~/Documentos")
TIME_FILE_PATH = os.path.join(DEFAULT_TIME_DIR, TIME_FILE_NAME)

def create_json() -> None:
    """
    If the JSON does not exist, it will create and use the current directory of the user 
    as a place to save the time file, being possible for the user 
    to change it if he wants to
    """
    if not os.path.exists(JSON_PATH):
        with open(JSON_PATH, "w") as file:
            json.dump(
                {"save_time_dir": TIME_FILE_PATH}, 
                file, 
                indent=2
            )

def save_in_json(path: str) -> None:
    """
    Saves the directory chosen by the user in the JSOn file

    - Params:
        - path (str): Path chosen by the user
    """
    if path:
        with open(JSON_PATH, "w") as file:
            json.dump({"save_time_dir": path}, file, indent=2)

def get_time_dir() -> str:
    """
    Gets the directory of the time file present in the JSON

    - Returns
        - path (str): path
    """
    with open(JSON_PATH, "r") as file:
        data = json.load(file)
        path = data.get("save_time_dir")
    return path

def get_time_data() -> List[str]:
    """
    Get data from time file

    - Returns
        - lines (list): Returns a list, 
        each element being a line from the file

    """
    time_dir = get_time_dir()
    with open(time_dir, "r") as fl:
        lines = fl.readlines()
    return lines
