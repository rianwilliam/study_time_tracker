import datetime

def save_time(time) -> None:

    actual_date = datetime.date.today().strftime("%d/%m/%Y")

    with open("study_time.txt", "a") as file:
        file.write(f"{actual_date}: {time} \n")

    return