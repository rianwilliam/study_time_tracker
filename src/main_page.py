import flet as ft
from src.conf.window_conf import window_conf
from src.widgets.page_widgets import Timer, conf_menu
from src.json_manager import create_json

def main(page: ft.Page) -> None:
    window_conf(page)
    create_json()
    timer = Timer()
    conf_menu(page)
    page.add(timer.widgets())
    page.update()