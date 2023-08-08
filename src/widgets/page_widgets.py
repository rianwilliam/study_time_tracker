"""Here are all the widgets that are added to the GUI"""
import time
from os import getcwd
from src.time_control import save_time
from src.json_manager import save_in_json
from src.widgets.charts import create_study_chart
from flet import (
    CrossAxisAlignment,
    MainAxisAlignment,
    ElevatedButton,
    border_radius,
    BottomSheet,
    FilePicker,
    IconButton,
    Container,
    alignment,
    Column,
    colors,
    icons,
    Page,
    Text,
    Row,
)

class Timer:
    """This class includes the timer and its functionalities"""

    def __init__(self) -> None:
        """
        Creates the time variables and the one 
        that determines if the timer is on or off
        """
        self.on = False
        self.seconds = 0
        self.minutes = 0
        self.hours = 0

    def change_state_widget(self, widget: any, disabled: bool) -> None:
        """
        Enables or disables the widget

        - Params:
            - widget: A widget from the flat library (Container, Row, IconButton,...)
            - disabled (bool): Whether the widget will be enabled or disabled
        """
        widget.disabled = disabled
        widget.update()

    def change_visibility_widget(self, widget: any, visible: bool) -> None:
        """
        Determines whether or not the widget will be

        - Params:
            - widget: A widget from the flat library (Container, Row, IconButton,...)
            - visible (bool): determines whether or not the widget will be visible
        """
        widget.visible = visible
        widget.update()
    
    def render(self, s: int, m: int, h: int) -> None:
        """
        Renders the time on the display every second
        
        - Params:
            - s (int): timer seconds
            - m (int): timer minutes
            - h (int): timer hours
        """
        self.display.value = f"{h:02d}:{m:02d}:{s:02d}"
        self.display.update()
    
    def get_time(self, e) -> None:
        """Get current time, perform save function and reset it"""
        self.on = False
        save_time(self.display.value)
        self.reset()
    
    def reset(self, e=None) -> None:
        """Reset timer variables and timer display"""
        self.display.value = "00:00:00"
        self.display.update()
        self.seconds, self.minutes, self.hours = 0,0,0
        self.change_visibility_widget(self.save_file_btn, visible=False)

    def stop(self, e=None) -> None:
        """
        Stop the timer, change the visibility of the save button, 
        disable the stop button and enable the start button
        """
        self.on = False
        self.seconds -= 1
        self.change_visibility_widget(self.save_file_btn, visible=True)
        self.change_state_widget(self.start_btn, disabled=False)
        self.change_state_widget(self.stop_btn, disabled=True)
        self.main_column.update()

    def start(self, e=None) -> None:
        """
        Start the timer, change the visibility of the save button 
        and disable the start button. 
        At each loop the variable value is rendered and displayed on the screen
        """
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
            self.render(self.seconds,self.minutes,self.hours)

    def widgets(self) -> Container:
        """
        Loads all timer interface widgets
        
        - Returns:
            - main_container (Container): A container containing all 
            the timer structure to be added on the page
        """
        self.display = Text(value="00:00:00",size=40,color=colors.BLACK)
        self.timer_container = Container(
            content=self.display,
            bgcolor=colors.WHITE,
            border_radius=border_radius.all(10),
            padding=10
        )
        self.start_btn = ElevatedButton(
            on_click=self.start, 
            text="Start", 
            bgcolor=colors.GREEN_700, 
            color=colors.WHITE
        )
        self.stop_btn = ElevatedButton(
            text="Stop", 
            on_click=self.stop, 
            bgcolor=colors.RED_700, 
            color=colors.WHITE
        )
        self.save_file_btn = ElevatedButton(
            text="Save time", 
            on_click=self.get_time, 
            visible=False, 
            bgcolor=colors.LIGHT_BLUE, 
            color=colors.WHITE
        )
        self.reset_btn = ElevatedButton(
            text="Reset",  
            on_click=self.reset,
            bgcolor=colors.WHITE, 
            color=colors.BLACK
        )
        self.controls_btns_column = Column(
            controls=[
                Row(
                    controls=[self.start_btn, self.stop_btn],
                    alignment="center"
                ),
                Row(
                    controls=[self.reset_btn, self.save_file_btn],
                    alignment="center"
                )
            ]
        )
        self.main_column = Column(
            controls=[
                self.timer_container,
                self.controls_btns_column
            ],
            alignment="center",
            horizontal_alignment="center"
        )
        self.main_container = Container(
            content=self.main_column,
            expand=True,
            alignment=alignment.center
        )
        return self.main_container
    
    def add_timer(self) -> Container:
        return self.widgets()

class DirectorySelector:
    """
    Adds the menu to select the directory where 
    the file with the times will be saved
    """

    def __init__(self, page: Page) -> None:
        """
        Create the directory picker, assign it the function that will be 
        executed after selecting the directory, and add it to the page

        - Params:
            - page (page): An instance of the Page class from the 
            flet library to which the directory picker will be added
        """
        self.directory_picker = FilePicker()
        self.directory_picker.on_result = self.save_path
        self.page = page
        self.page.add(self.directory_picker)

    def save_path(self,e) -> None:
        """Saves the directory in the JSON present in the user's /home"""
        save_in_json(self.directory_picker.result.path)

    def get_dir_selector(self) -> IconButton:
        """
        Gets the button that will activate directory selection
        
        - Returns
            - select_dir_btn (IconButton): Button that will activate 
            the directory picker
        """
        self.select_dir_btn = IconButton(
            icon=icons.SAVE_AS,
            icon_color=colors.WHITE,
            bgcolor=colors.BROWN,
            on_click=lambda _: self.directory_picker.save_file(
                file_name="study_time", 
                initial_directory=getcwd()
            )
        )
        return self.select_dir_btn

class BannerChart:
    """
    This is the menu that will display the type of graph 
    in which the data will be displayed
    """

    def __init__(self, page: Page) -> None:
        """
        Gets the page where the banner will be added

        - Params
            - page (Page):  An instance of the Page class from the 
            flet library to which the banner will be added
        """
        self.page = page

    def widgets(self) -> None:
        """Loads all timer interface widgets"""
        self.bar_chart = ElevatedButton(
            text="bar",
            icon=icons.BAR_CHART,
            on_click=lambda _: create_study_chart("bar")
        )
        self.plot_chart = ElevatedButton(
            text="plot",
            icon=icons.AREA_CHART,
            on_click=lambda _: create_study_chart("plot")
        )

    def add_banner(self) -> BottomSheet:
        """
        Here the banner will be created with the BottomSheet class of the flet

        - Returns
            - bottom_sheet (ElevatedButton): Button that will make the 
            menu appear at the bottom of the app
        """
        self.widgets()
        self.bottom_sheet = BottomSheet(
            Column(
                controls=[
                    Text("Choose view mode", text_align=alignment.center),
                    Row(
                        controls=[
                            self.bar_chart,
                            self.plot_chart
                        ],
                        alignment=MainAxisAlignment.SPACE_AROUND,
                    ),
                ],
                height=(self.page.window_height//6),
                horizontal_alignment=CrossAxisAlignment.CENTER,
                alignment=MainAxisAlignment.CENTER
            )
        )
        return self.bottom_sheet

    def open_dialog(self,e) -> None:
        """Function that opens the bottom sheet"""
        self.bottom_sheet.open = True
        self.page.update()

def conf_menu(page: Page) -> None:
    """
    This will be where all the menu containing configuration and 
    visualization elements will be built and added to the page.

    - Params:
        - page (Page):  An instance of the Page class from the 
        flet library to which the menu will be added

    """
    banner_chart = BannerChart(page)
    page.banner = banner_chart.add_banner()

    directory_picker = DirectorySelector(page)
    chart_btn = IconButton(
        icon=icons.ADD_CHART,
        icon_color=colors.WHITE,
        bgcolor=colors.BROWN,
        on_click=banner_chart.open_dialog
    )
    
    page.controls.append(
        Row(
            controls=[
                Container(
                    content=chart_btn
                ),
                Container(
                    content=directory_picker.get_dir_selector(),
                )
            ],
            alignment=MainAxisAlignment.SPACE_AROUND
        )
    )
    