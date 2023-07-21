import flet as ft
import time
from src.timelog import save_time

on = True
seconds = 0
minutes = 0
hours = 0

def timer(page: ft.Page):

    def render_time(s: int,m: int,h: int) -> None:
        display_timer.value = f"{h:02d}:{m:02d}:{s:02d}"
        display_timer.update()
    
    def get_time(e) -> None:
        global on, seconds, minutes, hours
        save_time(display_timer.value)

        seconds, minutes, hours = 0,0,0
        on = True
        save_file_btn.visible = False
        display_timer.value = "00:00:00"
        main_column.update()

    def disable_save_btn() -> None:
        save_file_btn.visible = False
        main_column.update()

    def reset_time(e) -> None:
        global seconds, minutes, hours
        seconds, minutes, hours = 0,0,0
        display_timer.value = "00:00:00"
        display_timer.update()
        disable_save_btn()

    def stop(e) -> None:
        global on
        global seconds
        seconds -= 1

        on = False
        save_file_btn.visible = True
        start_btn.disabled = False
        main_column.update()

    def start(e) -> None:
        global on
        global seconds, minutes, hours
        on = True

        disable_save_btn()

        while on:
            time.sleep(1)
            seconds += 1
            if seconds == 60:
                minutes += 1
                seconds = 0
            if minutes == 60:
                hours += 1
                minutes = 0
            render_time(seconds,minutes,hours)
    
    display_timer = ft.Text(value="00:00:00",size=40,color=ft.colors.BLACK)
    timer_container = ft.Container(
        content=display_timer,
        bgcolor=ft.colors.WHITE,
        border_radius=ft.border_radius.all(10),
        padding=10
    )
    start_btn = ft.ElevatedButton(
        on_click=start, 
        text="Start", 
        bgcolor=ft.colors.GREEN_700, 
        color=ft.colors.WHITE
    )
    stop_btn = ft.ElevatedButton(
        text="Stop", 
        on_click=stop, 
        bgcolor=ft.colors.RED_700, 
        color=ft.colors.WHITE
    )
    save_file_btn = ft.ElevatedButton(
        text="Save time", 
        on_click=get_time, 
        visible=False, 
        bgcolor=ft.colors.WHITE, 
        color=ft.colors.BLACK
    )
    reset_btn = ft.ElevatedButton(
        text="Reset",  
        on_click=reset_time,
        bgcolor=ft.colors.WHITE, 
        color=ft.colors.BLACK
    )
    control_btns_row = ft.Row(
        controls=[start_btn, stop_btn],
        alignment="center"
    )
    save_btns_row = ft.Row(
        controls=[reset_btn, save_file_btn],
        alignment="center"
    )
    main_column = ft.Column(
        controls=[
            timer_container,
            control_btns_row,
            save_btns_row
        ],
        alignment="center",
        horizontal_alignment="center"
    )
    main_container = ft.Container(
        content=main_column,
        expand=True,
        alignment=ft.alignment.center
    )
    return main_container

def conf_menu(page: ft.Page):

    def open_menu(e) -> None:
        page.dialog = dialog_menu
        dialog_menu.open = True
        page.update()

    def close_menu(e) -> None:
        dialog_menu.open = False
        page.update()

    directory_selector = ft.FilePicker()
    select_directory_btn = ft.ElevatedButton(
        text="Select directory", 
        on_click= lambda _: directory_selector.save_file(
            file_name="study_time", 
            initial_directory="."
        )
    )
    directory_selector.on_result = ""

    close_dialog_btn = ft.IconButton(icon=ft.icons.CLOSE, on_click=close_menu)
    dialog_menu = ft.AlertDialog(
        modal=True,
        actions=[close_dialog_btn,select_directory_btn,directory_selector],
        actions_alignment=ft.MainAxisAlignment.CENTER,
        actions_padding=20
    )
    menu_btn = ft.IconButton(icon=ft.icons.QUESTION_MARK, on_click=open_menu)
 
    page.appbar = ft.AppBar(actions=[menu_btn])