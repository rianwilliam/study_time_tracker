"""Main page where all app elements will be added"""
import flet as ft
from src.json_manager import create_json
from src.conf.window_conf import set_screen_size
from src.widgets.page_widgets import Timer, conf_menu

def main(page: ft.Page) -> None:
    set_screen_size(page)
    create_json()
    conf_menu(page)
    timer = Timer()
    
    page.add(timer.add_timer())
    page.update()