from tkinter import Tk
from flet import Page, ThemeMode

def window_conf(page: Page) -> None:
    root = Tk()
    root.withdraw()
    screen_width = page.window_width
    screen_height = page.window_height
    root.destroy()
    
    page.window_center()
    page.spacing = 1
    page.title = "Study hours"
    page.theme_mode = ThemeMode.DARK
    page.window_max_width = int(screen_width / 3.9)
    page.window_max_height = int(screen_height / 2.0)
    page.window_min_width = int(screen_width / 3.8)
    page.window_min_height = int(screen_height / 1.9)


