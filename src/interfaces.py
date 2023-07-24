import flet as ft
import time
from os.path import dirname
from src.timelog import save_time
from src.json_manager import save_in_json

class Timer:

    def __init__(self) -> None:
        self.on = False
        self.seconds = 0
        self.minutes = 0
        self.hours = 0
    
    def render_time(self, s: int, m: int, h: int) -> None:
        self.display.value = f"{h:02d}:{m:02d}:{s:02d}"
        self.display.update()
    
    def get_time(self, e) -> None:
        self.on = False
        save_time(self.display.value)
        self.reset_time()
    
    def reset_time(self, e=None) -> None:
        self.seconds, self.minutes, self.hours = 0,0,0
        self.display.value = "00:00:00"
        self.display.update()
        self.change_visibility_widget(self.save_file_btn, visible=False)

    def change_state_widget(self, widget: any, disabled: bool) -> None:
        widget.disabled = disabled
        widget.update()

    def change_visibility_widget(self, widget: any, visible: bool) -> None:
        widget.visible = visible
        widget.update()

    def stop(self, e) -> None:
        self.on = False
        self.seconds -= 1
        self.change_visibility_widget(self.save_file_btn, visible=True)
        self.change_state_widget(self.start_btn, disabled=False)
        self.change_state_widget(self.stop_btn, disabled=True)
        self.main_column.update()

    def start(self, e) -> None:
        self.on = True
        self.change_visibility_widget(self.save_file_btn, visible=False)
        self.change_state_widget(self.stop_btn, disabled=False)
        self.change_state_widget(self.start_btn, disabled=True)

        while self.on:
            time.sleep(1)
            self.seconds += 1
            if self.seconds == 60:
                self.minutes += 1
                self.seconds = 0
            if self.minutes == 60:
                self.hours += 1
                self.minutes = 0
            self.render_time(self.seconds,self.minutes,self.hours)


    def widgets(self):
        self.display = ft.Text(value="00:00:00",size=40,color=ft.colors.BLACK)
        self.timer_container = ft.Container(
            content=self.display,
            bgcolor=ft.colors.WHITE,
            border_radius=ft.border_radius.all(10),
            padding=10
        )
        self.start_btn = ft.ElevatedButton(
            on_click=self.start, 
            text="Start", 
            bgcolor=ft.colors.GREEN_700, 
            color=ft.colors.WHITE
        )
        self.stop_btn = ft.ElevatedButton(
            text="Stop", 
            on_click=self.stop, 
            bgcolor=ft.colors.RED_700, 
            color=ft.colors.WHITE
        )
        self.save_file_btn = ft.ElevatedButton(
            text="Save time", 
            on_click=self.get_time, 
            visible=False, 
            bgcolor=ft.colors.WHITE, 
            color=ft.colors.BLACK
        )
        self.reset_btn = ft.ElevatedButton(
            text="Reset",  
            on_click=self.reset_time,
            bgcolor=ft.colors.WHITE, 
            color=ft.colors.BLACK
        )
        self.controls_btns_column = ft.Column(
            controls=[
                ft.Row(
                    controls=[self.start_btn, self.stop_btn],
                    alignment="center"
                ),
                ft.Row(
                    controls=[self.reset_btn, self.save_file_btn],
                    alignment="center"
                )
            ]
        )
        self.main_column = ft.Column(
            controls=[
                self.timer_container,
                self.controls_btns_column
            ],
            alignment="center",
            horizontal_alignment="center"
        )
        self.main_container = ft.Container(
            content=self.main_column,
            expand=True,
            alignment=ft.alignment.center
        )
        return self.main_container

def conf_menu(page: ft.Page):

    def open_menu(e) -> None:
        page.dialog = dialog_menu
        dialog_menu.open = True
        page.update()

    def close_menu(e) -> None:
        dialog_menu.open = False
        page.update()

    directory_selector = ft.FilePicker()
    directory_selector.on_result = lambda _: save_in_json({"save_time_dir": directory_selector.result.path})

    select_dir_text = ft.Text(
        value="Select the directory where the file with time will be saved",
        text_align="center"
    )
    select_dir_btn = ft.ElevatedButton(
        text="Select directory", 
        on_click= lambda _: directory_selector.save_file(
            file_name="study_time",
            initial_directory=dirname(__file__)
        )
    )
    dialog_row = ft.Row(
        controls=[select_dir_text, select_dir_btn],
        wrap=True,
        alignment="center"
    )
    close_dialog_btn = ft.IconButton(icon=ft.icons.CLOSE, on_click=close_menu)
    dialog_menu = ft.AlertDialog(
        modal=True,
        actions=[close_dialog_btn,dialog_row,directory_selector],
        actions_alignment=ft.MainAxisAlignment.CENTER,
        actions_padding=20
    )
    menu_btn = ft.IconButton(icon=ft.icons.QUESTION_MARK, on_click=open_menu)
    page.appbar = ft.AppBar(actions=[menu_btn])
    