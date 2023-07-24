import os
import re
from datetime import date, timedelta
from src.json_manager import get_json_data
from typing import Dict

def format_time(time):
    formatted_time = time.split(":")
    return [int(x) for x in formatted_time]

def sum_time(saved_time: str, time: str):
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

    if os.path.exists(json_data["save_time_dir"]):
        with open(json_data["save_time_dir"], "r") as file:
            lines = file.readlines()
            if lines:
                if actual_date in lines[-1]:
                    time = sum_time(lines[-1], time)
                    lines.pop()
                    with open(json_data["save_time_dir"], "w") as file:
                        file.writelines(lines)

    with open(json_data["save_time_dir"], "a") as file:
        file.write(f"{actual_date}: {time} \n")