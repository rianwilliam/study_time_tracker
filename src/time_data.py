import os
import re
from typing import List
from datetime import date, timedelta
from src.json_manager import get_json_data

def format_time(time: str) -> List[int]:
    formatted_time = time.split(":")
    return [int(x) for x in formatted_time]

def sum_time(saved_time: str, time: str) -> str:
    saved_time = re.findall(r"[0-9]\:[0-9]{2}\:[0-9]{2}", saved_time)[0]
    saved_h, saved_m, saved_s = format_time(saved_time)
    h, m, s = format_time(time)

    total_time = (
        timedelta(hours=saved_h,minutes=saved_m,seconds=saved_s) + \
        timedelta(hours=h,minutes=m,seconds=s)
    )
    return total_time

def save_time(time) -> None:
    actual_date = date.today().strftime("%d/%m/%Y")
    json_data = get_json_data()
    time_file_path = json_data["save_time_dir"]

    if os.path.exists(time_file_path):
        with open(time_file_path, "r") as file:
            lines = file.readlines()
            most_recent_line = lines[-1]
            if lines and actual_date in most_recent_line:
                time = sum_time(most_recent_line, time)
                lines.pop()
                with open(time_file_path, "w") as file:
                    file.writelines(lines)
                    
    with open(time_file_path, "a") as file:
        file.write(f"{actual_date}: {time} \n")