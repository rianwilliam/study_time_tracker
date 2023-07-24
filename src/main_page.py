import flet as ft
from src.conf.window_conf import window_conf
from src.interfaces import Timer, conf_menu

def main(page: ft.Page) -> None:
    window_conf(page)
    timer = Timer()

    conf_menu(page)
    page.add(timer.widgets())
    page.update()