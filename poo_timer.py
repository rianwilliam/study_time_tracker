import flet as ft
import time
from os.path import dirname
from src.timelog import save_time


on = True
seconds = 0
minutes = 0
hours = 0

def timer():

    def render_time(s: int,m: int,h: int) -> None:
        display.value = f"{h:02d}:{m:02d}:{s:02d}"
        display.update()
    
    def get_time(e) -> None:
        global on, seconds, minutes, hours
        save_time(display.value)

        seconds, minutes, hours = 0,0,0
        on = True
        display.value = "00:00:00"
        change_visibility_widget(save_file_btn, visible=False)
        main_column.update()

    def change_state_widget(widget: any, disabled: bool) -> None:
        widget.disabled = disabled
        widget.update()

    def change_visibility_widget(widget: any, visible: bool) -> None:
        widget.visible = visible
        widget.update()

    def reset_time(e) -> None:
        global seconds, minutes, hours
        seconds, minutes, hours = 0,0,0
        display.value = "00:00:00"
        display.update()
        change_visibility_widget(save_file_btn, visible=False)

    def stop(e) -> None:
        global on
        global seconds
        seconds -= 1

        on = False
        change_visibility_widget(save_file_btn, visible=True)
        change_state_widget(start_btn, disabled=False)
        change_state_widget(stop_btn, disabled=True)
        main_column.update()

    def start(e) -> None:
        global on
        global seconds, minutes, hours
        on = True

        change_visibility_widget(save_file_btn, visible=False)
        change_state_widget(stop_btn, disabled=False)
        change_state_widget(start_btn, disabled=True)

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
    
    display = ft.Text(value="00:00:00",size=40,color=ft.colors.BLACK)
    timer_container = ft.Container(
        content=display,
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
    controls_btns_column = ft.Column(
        controls=[
            ft.Row(
                controls=[start_btn, stop_btn],
                alignment="center"
            ),
            ft.Row(
                controls=[reset_btn, save_file_btn],
                alignment="center"
            )
        ]
    )
    main_column = ft.Column(
        controls=[
            timer_container,
            controls_btns_column
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
