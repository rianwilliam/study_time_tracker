import flet as ft
import time
from os import getcwd
from src.time_control import save_time
from src.json_manager import save_in_json
from src.widgets.charts import create_study_chart

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
        self.display.value = "00:00:00"
        self.seconds, self.minutes, self.hours = 0,0,0
        self.display.update()
        self.change_visibility_widget(self.save_file_btn, visible=False)

    def change_state_widget(self, widget: any, disabled: bool) -> None:
        widget.disabled = disabled
        widget.update()

    def change_visibility_widget(self, widget: any, visible: bool) -> None:
        widget.visible = visible
        widget.update()

    def stop(self, e=None) -> None:
        self.on = False
        self.seconds -= 1
        self.change_visibility_widget(self.save_file_btn, visible=True)
        self.change_state_widget(self.start_btn, disabled=False)
        self.change_state_widget(self.stop_btn, disabled=True)
        self.main_column.update()

    def start(self, e=None) -> None:
        self.on = True
        self.change_visibility_widget(self.save_file_btn, visible=False)
        self.change_state_widget(self.stop_btn, disabled=False)
        self.change_state_widget(self.start_btn, disabled=True)

        while self.on:
            self.seconds += 1
            if self.seconds == 60:
                self.minutes += 1
                self.seconds = 0
            if self.minutes == 60:
                self.hours += 1
                self.minutes = 0
            time.sleep(1)
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
            bgcolor=ft.colors.LIGHT_BLUE, 
            color=ft.colors.WHITE
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

class DirectorySelector:

    def __init__(self, page: ft.Page) -> None:
        self.directory_selector = ft.FilePicker()
        self.directory_selector.on_result = self.file_picker_result
        self.page = page
        self.page.add(self.directory_selector)

    def file_picker_result(self,e):
        save_in_json({"save_time_dir": self.directory_selector.result.path})

    def dir_btn(self):
        self.select_dir_btn = ft.IconButton(
            icon=ft.icons.SAVE_AS,
            icon_color=ft.colors.WHITE,
            bgcolor=ft.colors.BROWN,
            on_click=lambda _: self.directory_selector.save_file(
                file_name="study_time", 
                initial_directory=getcwd()
            )
        )
        return self.select_dir_btn
#! Consertar o dialog
#! Colocar o método de add no timer, igual fiz na classe abaixo
#! Consertar o alinhamento do dialog
#! Trocar o icone de abrir o dialog para ADD_CHART 

class DialogChart:

    def __init__(self, page: ft.Page) -> None:
        self.page = page

    def widgets(self):
        self.bar_chart = ft.ElevatedButton(
            text="bar",
            icon=ft.icons.BAR_CHART,
            on_click=lambda _: create_study_chart("bar")
        )
        self.plot_chart = ft.ElevatedButton(
            text="plot",
            icon=ft.icons.AREA_CHART,
            on_click=lambda _: create_study_chart("plot")
        )

    def add_dialog(self):
        self.widgets()
        self.bottom_sheet = ft.BottomSheet(
            ft.Column(
                controls=[
                    ft.Text("Choose view mode", text_align=ft.alignment.center),
                    ft.Row(
                        controls=[
                            self.bar_chart,
                            self.plot_chart
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                    ),
                ],
                height=(self.page.window_height // 6),
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER
            )
        )
        return self.bottom_sheet

    def open_dialog(self,e):
        self.bottom_sheet.open = True
        self.page.update()

def conf_menu(page: ft.Page):
    dialog_chart = DialogChart(page)
    page.banner = dialog_chart.add_dialog()

    directory_selector = DirectorySelector(page)
    chart_btn = ft.IconButton(
        icon=ft.icons.ADD_CHART,
        icon_color=ft.colors.WHITE,
        bgcolor=ft.colors.BROWN,
        on_click=dialog_chart.open_dialog
    )
    
    page.controls.append(
        ft.Row(
            controls=[
                ft.Container(
                    content=chart_btn
                ),
                ft.Container(
                    content=directory_selector.dir_btn(),
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND
        )
    )
    