import flet as ft
from src.conf.window_conf import window_conf
from src.interfaces import Timer, conf_menu
from src.json_manager import make_json

def main(page: ft.Page) -> None:
    window_conf(page)
    make_json()
    timer = Timer()

    conf_menu(page)
    page.add(timer.widgets())
    page.update()