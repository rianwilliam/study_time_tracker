"""Perform screen adjustment functions"""
import platform
from tkinter import Tk
from flet import Page, ThemeMode

def set_screen_size(page: Page) -> None:
    """
    Performs screen resizing according to the user's screen size
    
    - Params:
        - page (Page): A page instance of the flet library    
    """
    root = Tk()
    root.withdraw()
    screen_width = page.window_width
    screen_height = page.window_height
    root.destroy()
    
    page.title = "Stopwatch"
    page.theme_mode = ThemeMode.DARK
    page.spacing = 1
    page.window_center()

    if platform.system() == "Linux":
        page.window_max_width = screen_width//3.9
        page.window_max_height = screen_height//2.0
        page.window_min_width = screen_width//3.8
        page.window_min_height = screen_height//1.9
    elif platform.system() == "Windows":
        page.window_resizable = False
        page.window_width = screen_width//3.8
        page.window_height = screen_height//1.9