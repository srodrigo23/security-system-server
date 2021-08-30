import socket
from loger import print_log

from settings import Settings
from clients import Clients
from nodes import Nodes

class Server:
    
    def __init__(self):
        
        self.settings = Settings()
        self.server_ready = False
            
    def run(self):
        self.server_ready = True
        self.launch_clients()
        self.run_server()
        
    def launch_clients(self):
        self.clients_thread = Clients(self.settings)
        self.clients_thread.start()
        self.nodes_thread = Nodes(self.settings)
        self.nodes_thread.start()
                          
    def run_server(self):
        print_log('i', 'Server running...')
        try:
            while self.server_ready:
                """
                run while server threads are running
                """
        except KeyboardInterrupt: # close all threads
            print_log('e', 'Server interrupted...')
            self.server_ready = False
            self.stop_clients_thread()
            self.stop_nodes_thread()

    def stop_clients_thread(self):
        print_log('i', 'Stopping all clients comunication...')
        self.clients_thread.clients_ready = False
        self.clients_thread.close_clients_connection()
        self.clients_thread.join(1)
    
    def stop_nodes_thread(self):
        print_log('i', 'Stopping all nodes comunication...')
        self.nodes_thread.nodes_ready = False
        self.nodes_thread.close_nodes_connection()
        self.nodes_thread.join(1)
