from flet import Page, ThemeMode
import flet as ft
import tkinter as tk

def window_conf(page: Page) -> None:
    root = tk.Tk()
    root.withdraw()
    screen_width = page.window_width
    screen_height = page.window_height
    root.destroy()
    
    page.title = "Study hours"
    page.theme_mode = ThemeMode.DARK
    page.window_center()
    page.window_max_width = int(screen_width / 3.1)
    page.window_max_height = int(screen_height / 1.9)
    page.window_min_width = int(screen_width / 3)
    page.window_min_height = int(screen_height / 1.8)


