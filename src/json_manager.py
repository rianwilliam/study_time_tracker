import os
import json
from typing import Dict

user_dir = os.path.expanduser("~")
file_name = "study_data.json"
JSON_PATH = os.path.join(user_dir, file_name)

def save_in_json(info: Dict) -> None:
    with open(JSON_PATH, "w") as file:
        json.dump(info, file, indent=2)

def get_json_data() -> Dict:
    with open(JSON_PATH, "r") as file:
        data = json.load(file)
    return data