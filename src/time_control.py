"""Responsible for adding content to the text file"""
import os
import re
from typing import List
from datetime import date, timedelta
from src.json_manager import get_time_dir

def time_to_int_list(time: str) -> List[int]:
    """
    Gets the time and divides it into 
    hours, minutes and seconds within a list
    in integer format
    
    - Params:
        - time (str): Time in string format

    - Returns:
        - formatted_time (list): List with 
        time in integer format
    """
    time_list = time.split(":")
    formatted_time = [int(x) for x in time_list]
    return formatted_time

def sum_time(saved_time: str, time: str) -> str:
    """
    Performs the sum of the time if there is already 
    some time recorded on the same date
    
    - Params:
        - saved_time (str): Content saved to the most 
        recent line of the text file

        - time (str): New time to be added to 
        the existing one
    """
    saved_time = re.findall(r"[0-9]+\:[0-9]+\:[0-9]+", saved_time)[0]
    saved_h, saved_m, saved_s = time_to_int_list(saved_time)
    h, m, s = time_to_int_list(time)

    total_time = (
        timedelta(hours=saved_h,minutes=saved_m,seconds=saved_s) + \
        timedelta(hours=h,minutes=m,seconds=s)
    )
    return total_time

def get_current_week_day() -> str:
    """
    Get the current day of the week using the datetime library
    
    - Returns: 
        - week_day (str): Day of the week spelled out
    """
    week = [
            "Monday", 
            "Tuesday", 
            "Wednesday", 
            "Thursday", 
            "Friday", 
            "Saturday", 
            "Sunday"
        ]
    week_day = week[date.weekday(date.today())]
    return week_day

def save_time(time: str) -> None:
    """
    Saves time to file, along with current date and day of week.
    If there is already a time on the same date, 
    it will rewrite the last line with the sum of the new time and 
    the already saved time

    - Params:
        - time (str): display time
    """
    current_date = date.today().strftime("%d/%m/%Y")
    week_day = get_current_week_day()    
    time_file_path = get_time_dir()

    if os.path.exists(time_file_path):
        with open(time_file_path, "r") as fl:
            lines = fl.readlines()
            most_recent_line = lines[-1]
            if lines and current_date in most_recent_line:
                time = sum_time(most_recent_line, time)
                lines.pop()
                with open(time_file_path, "w") as fl:
                    fl.writelines(lines)
                    
    with open(time_file_path, "a") as fl:
        fl.write(f"{current_date} - {week_day}: {time} \n")