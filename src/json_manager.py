import os
import json
from typing import Dict

user_dir = os.path.expanduser("~")
file_json_name = "study_data.json"
JSON_PATH = os.path.join(user_dir, file_json_name)
study_file_name = "study_time.txt"

def create_json() -> None:
    if not os.path.exists(JSON_PATH):
        with open(JSON_PATH, "w") as file:
            json.dump(
                {"save_time_dir": f"{os.getcwd()}/{study_file_name}"}, 
                file, 
                indent=2
            )

def save_in_json(info: Dict) -> None:
    if info.get("save_time_dir"):
        with open(JSON_PATH, "w") as file:
            json.dump(info, file, indent=2)

def get_json_data() -> Dict:
    with open(JSON_PATH, "r") as file:
        data = json.load(file)
    return data

def get_file_time_dir():
    with open(JSON_PATH, "r") as file:
        data = json.load(file)
        path = data.get("save_time_dir")
    return  path