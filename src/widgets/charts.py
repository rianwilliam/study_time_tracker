import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from src.json_manager import get_file_time_dir
import re
import flet as ft

def extract_hours(times: str):
    hours = []
    for time in times:
        time = time.split(":")
        hours.append(int(time[0]))
    return hours

def create_study_chart(chart_type: str) -> None:
    file_time_dir = get_file_time_dir()

    with open(file_time_dir, "r") as ft:
        lines = ft.readlines()
        dates = re.findall(r"[0-9]{2}\/[0-9]{2}\/[0-9]{2}", " ".join(lines))
        time = re.findall(r"[0-9]\:[0-9]{2}\:[0-9]{2}", " ".join(lines))
    hours = extract_hours(time)

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
    
    # * Opção de salvar gráfico
    # plt.savefig('grafico_de_barras.png', bbox_inches='tight')

