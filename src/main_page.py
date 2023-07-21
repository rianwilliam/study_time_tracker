import time
import flet as ft
from src.window_conf import window_conf
from src.interfaces import timer, conf_menu

def main(page: ft.Page) -> None:
    window_conf(page)

    conf_menu(page)
    page.add(timer(page))
    page.update()