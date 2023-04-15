from tcp_server import TCPServer

# from mail import test_mail

from view.main_screen import MainScreen
from view.main_screen import Controller

if __name__ == "__main__":
    controller = Controller()
    main_screen = MainScreen(controller=controller)
    controller.set_view(view=main_screen)
    main_screen.mainloop()
    

    # tcp_server = TCPServer()
    # tcp_server.prepare_server()
    # tcp_server.run()
    