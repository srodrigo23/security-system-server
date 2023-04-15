
import tkinter as tk

from tkinter import *
    # from tkinter.ttk import Button

class ControlPanel(LabelFrame):

    def __init__(self, parent, controller)-> None:
        LabelFrame.__init__(self=self, master=parent)
        self.message = "Control Panel"
        self.controller = controller 
        self.setup()

    def setup(self)-> None:
        self.config(text=self.message)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        label_execution =  Label(
            master=self, 
            text="Execution")
        label_execution.grid(
            row=0, column=0, 
            rowspan=1, columnspan=1, 
            padx=2, pady=2, 
            sticky='ew'
        )

        config_button = Button(
            master=self, 
            compound='left',
            text="Configuration",
            command=lambda:self.controller.make_something()
        )
        config_button.grid(
            row=0, column=2,
            rowspan=1, columnspan=1, 
            padx=2, pady=2, 
            sticky='ew'
        )

        swith_server = Button(
            master=self, 
            compound='left',
            text="Configuration",
            command=lambda:self.controller.make_something()
        )

        swith_server.grid(
            row=0, column=1,
            rowspan=1, columnspan=1, 
            padx=2, pady=2, 
            sticky='ew'
        )
    def swith_button(self)->None:
        pass


class MainScreen(tk.Tk):

    def __init__(self, controller) -> None:
        super().__init__()
        self.width = 500
        self.height = 500
        self.isResizable = False
        self.controller  = controller
        self.maintitle = "Server"
        self.setup()
        self.setup_exit_menu()
        self.setup_control_panel()


    def setup(self) -> None:
        self.title(self.maintitle)
        self.geometry(f'{self.width}x{self.height}')
        # self.resizable(self.isResizable, self.isResizable)
        # self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        # self.columnconfigure(2, weight=1)
        # self.rowconfigure(0, weight=0)
    
    def setup_control_panel(self) -> None:
        control_panel = ControlPanel(
            parent=self,
            controller=self.controller
        )
        control_panel.grid(row=0, column=0, rowspan=1, columnspan=4, padx=5, pady=5, sticky='new')
    
    def setup_exit_menu(self)->None:
        self.__menubar__ = tk.Menu(self)
        self.config(menu=self.__menubar__)
        file_menu = tk.Menu(self.__menubar__)
        file_menu.add_command(label='Exit', command=self.destroy)
        self.__menubar__.add_cascade(label='File', menu=file_menu)
        self.resizable(False, False)

            
class Controller:
    def __init__(self) -> None:
        pass

    def make_something(self) -> None:
        print('Damas gratis!!')


class ToggleButton(Button):

    def __init__(self, parent, function) -> None:
        super().__init__(self=self, master=parent, command=function)
        # (self=self, master=parent)
        self.image_on = PhotoImage(file = "../img/on.png")
        self.image_off = PhotoImage(file = "../img/off.png")
        self.isOn = False

    def switch(self) -> None:
        pass
        # self.config(image=)
