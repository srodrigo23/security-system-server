import cv2
import socket
import logging

from settings import Settings
from connection import Connection

class Server():
    
    def __init__(self):
        self.settings = Settings()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = self.settings.get_host_address()
        self.port = self.settings.get_port()
        self.nodes = [] # to manage conections
        self.clients = []
        self.server_ready = False
        
    def run(self):
        self.prepare()
        self.init_server()        
        self.listen_connections()
        self.close_server()
    
    def prepare(self):
        if is_host_port_in_use(self.host, self.port):
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    def init_server(self):
        print("Welcome Security Server ")
        try:
            self.socket.bind((self.host, self.port))
            self.socket.listen(self.settings.get_num_clients())
            self.server_ready = True
        except socket.error as e:
            print(f"Error on init server : {str(e)}")
            
    def listen_connections(self):
        while self.server_ready:
            try:
                conn, addr = self.socket.accept()
                self.nodes.append(Connection(conn, addr))
                self.nodes[len(self.nodes)-1].start()
            except socket.error as e:
                self.server_ready = False
                printl(f'Error on Listen connection : {str(e)}')
                
    def close_server(self):
        print('Server turned off')
        try:
            self.socket.close()
        except socket.error as e:
            print(f'Error on Close server {str(e)}')
            

def is_host_port_in_use(host, port):
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, port)) == 0
