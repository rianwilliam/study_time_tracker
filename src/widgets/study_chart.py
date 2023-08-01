import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from src.json_manager import get_file_time_dir
import re

# Dados de exemplo

def extract_hours(times: str):
    hours = []
    for time in times:
        time = time.split(":")
        hours.append(int(time[0]))
    return hours

def create_study_chart(e):
    file_time_dir = get_file_time_dir()

    with open(file_time_dir, "r") as ft:
        lines = ft.readlines()
        dates = re.findall(r"[0-9]{2}\/[0-9]{2}\/[0-9]{2}", " ".join(lines))
        time = re.findall(r"[0-9]\:[0-9]{2}\:[0-9]{2}", " ".join(lines))
    hours = extract_hours(time)
    fig, ax = plt.subplots()
    ax.bar(dates, hours)

    #* Modos de visualização de gráfico
    # ax.plot(dates, hours)
    # ax.step(dates, hours)
    # ax.stackplot(dates, hours)
    # ax.stem(dates, hours)


    ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
    ax.set_yticks(range(24))

    plt.xticks(rotation=45)

    plt.ylim(0, 24)

    plt.xlabel("Datas")
    plt.ylabel("Horas")

    plt.title('Rendimento de estudo')

    #* Opção de salvar gráfico
    # plt.savefig('grafico_de_barras.png', bbox_inches='tight')
    plt.tight_layout()
    plt.show()
