import os
import re
from typing import List
from datetime import date, timedelta
from src.json_manager import get_file_time_dir

def format_time(time: str) -> List[int]:
    formatted_time = time.split(":")
    return [int(x) for x in formatted_time]

def sum_time(saved_time: str, time: str) -> str:
    saved_time = re.findall(r"[0-9]+\:[0-9]+\:[0-9]+", saved_time)[0]
    saved_h, saved_m, saved_s = format_time(saved_time)
    h, m, s = format_time(time)

    total_time = (
        timedelta(hours=saved_h,minutes=saved_m,seconds=saved_s) + \
        timedelta(hours=h,minutes=m,seconds=s)
    )
    return total_time

def save_time(time) -> None:
    current_date = date.today().strftime("%d/%m/%Y")
    days = [
        "Segunda", 
        "Terça", 
        "Quarta", 
        "Quinta", 
        "Sexta", 
        "Sábado", 
        "Domingo"
    ]
    current_week_day = days[date.weekday(date.today())]

    time_file_path = get_file_time_dir()
    print(time_file_path)

    if os.path.exists(time_file_path):
        with open(time_file_path, "r") as tf:
            lines = tf.readlines()
            most_recent_line = lines[-1]
            if lines and current_date in most_recent_line:
                time = sum_time(most_recent_line, time)
                lines.pop()
                with open(time_file_path, "w") as tf:
                    tf.writelines(lines)
                    
    with open(time_file_path, "a") as file:
        file.write(f"{current_date} - {current_week_day}: {time} \n")