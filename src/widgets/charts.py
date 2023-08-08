"""
Here the graph will be built to visualize the hours saved in 
each day of use of the app
"""
import re
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from src.json_manager import get_time_data
from src.time_control import time_to_int_list

def extract_hours(times: str) -> None:
    """
    Get the string with all the times 
    and extract the hours from each one

    - Params
        - times (str): A string containing all times 
        recorded in the text file
    
    - Returns:
        - hours (list): A list containing all hours in 
        integer format
    """
    hours = []
    for time in times:
        time_list = time_to_int_list(time)
        hours.append(time_list[0])
    return hours

def create_study_chart(chart_type: str) -> None:
    """
    Get dates and times saved in the text file and 
    create a graph with the mathplot lib library to 
    visualize the hours of each day the app was used
    
    - Params: 
        - char_type (str): Determines what type of chart the 
        visualization will be on
    """
    time_data = get_time_data()
    dates = re.findall(r"[0-9]+\/[0-9]+\/[0-9]+", " ".join(time_data))
    times = re.findall(r"[0-9]+\:[0-9]+\:[0-9]+", " ".join(time_data))
    hours = extract_hours(times)

    plt.rcParams["toolbar"] = "None"
    fig, ax = plt.subplots()

    match chart_type:
        case "plot":
            ax.plot(dates, hours)
        case "bar":
            ax.bar(dates, hours)

    ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
    ax.set_yticks(range(24)) 
    plt.xticks(rotation=45)
    plt.ylim(0, 24)
    plt.xlabel("Datas")
    plt.ylabel("Horas")
    plt.title('Rendimento de estudo')
    plt.tight_layout()
    plt.show()


