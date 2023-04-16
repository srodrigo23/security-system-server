
import tkinter as tk
from tkinter import *

class ControlPanel(LabelFrame):

    def __init__(self, parent, controller)-> None:
        LabelFrame.__init__(self=self, master=parent)
        self.message = "Control Panel"
        self.controller = controller
        self.is_on = False
        self.setup()
        # self.setup_swith_button()

    def setup(self)-> None:
        self.config(text=self.message)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.swith_server_button = Button(
            master=self, 
            compound='left',
            text="Server On",
            command=lambda:self.controller.manage_server()
        )
        self.swith_server_button.grid(
            row=0, column=0,
            rowspan=1, columnspan=1, 
            padx=2, pady=2, 
            sticky='ew'
        )
        # label_execution =  Label(
        #     master=self, 
        #     text="Execution :")
        # label_execution.grid(
        #     row=0, column=0, 
        #     rowspan=1, columnspan=1, 
        #     padx=2, pady=2, 
        #     sticky='ew'
        # )

        config_button = Button(
            master=self, 
            compound='left',
            text="Configuration",
            command=lambda:self.controller.make_something()
        )
        config_button.grid(
            row=0, column=1,
            rowspan=1, columnspan=1, 
            padx=2, pady=2, 
            sticky='ew'
        )
        # self.swith_server.config(command=lambda:swith_button(is_on=self.is_on,button=self.swith_server))


class MainScreen(tk.Tk):

    def __init__(self, controller) -> None:
        super().__init__()
        self.width = 500
        self.height = 500
        self.isResizable = True
        self.controller  = controller
        self.maintitle = "Server"
        self.setup()
        self.setup_exit_menu()
        self.setup_control_panel()


    def setup(self) -> None:
        self.title(self.maintitle)
        self.geometry(f'{self.width}x{self.height}')
        self.resizable(self.isResizable, self.isResizable)
        # self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        # self.columnconfigure(2, weight=1)
        # self.rowconfigure(0, weight=0)
    
    def setup_control_panel(self) -> None:
        self.control_panel = ControlPanel(
            parent=self,
            controller=self.controller.server_controller
        )
        self.control_panel.grid(
            row=0, column=0, 
            rowspan=1, columnspan=4, 
            padx=5, pady=5, sticky='new')
    
    def setup_exit_menu(self)->None:
        self.__menubar__ = tk.Menu(self)
        self.config(menu=self.__menubar__)
        file_menu = tk.Menu(self.__menubar__)
        file_menu.add_command(label='Exit', command=self.destroy)
        self.__menubar__.add_cascade(label='File', menu=file_menu)

            
class Controller:

    def __init__(self) -> None:
        self.view = None
        self.server_controller = ServerController()

    def make_something(self) -> None:
        print('Damas gratis!!')

    def set_view(self, view) ->None:
        self.view = view
        self.server_controller.set_view(view=view.control_panel)


from tcp_server import TCPServer
from threading import Thread

class ServerController():

    def __init__(self) -> None:
        self.is_on = False
        self.view = None

    def set_view(self, view) -> None:
        self.view = view

    def manage_server(self) ->None:
        if self.is_on:
            print('apagar')
            self.view.swith_server_button.config(text="Server On")
            self.is_on = False
        else:
            print('encender')
            self.view.swith_server_button.config(text="Server Off")
            self.is_on = True

            # self.tcp_server = TCPServer()
            # self.tcp_server.prepare_server()
            # self.tcp_server.run()
            # import multiprocessing
            # proc = multiprocessing.Process( self.tcp_server.run(), () )
            # proc.start()

            self.thread = Thread(
                target=self.tcp_server.run(),
                args=()
            )
            self.thread.daemon=True
            self.thread.start()
            # print('llega aqui')
    
    