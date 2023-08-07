import flet as ft
from src.json_manager import create_json
from src.conf.window_conf import set_screen_size
from src.widgets.page_widgets import Timer, conf_menu

def main(page: ft.Page) -> None:
    set_screen_size(page)
    create_json()
    timer = Timer()
    conf_menu(page)
    
    page.add(timer.widgets())
    set_screen_size(page)
    page.update()