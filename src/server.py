import cv2
import socket
import logging
from settings import Settings
from connection import Connection

# from image_hub import ImageHub

class Server():
    
    def __init__(self):
        self.settings = Settings()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = self.settings.get_host_address()
        self.port = self.settings.get_port()
        
        self.nodes = [] # to manage conections
        self.clients = []
        self.nodes_i = 0
        
        self.init_server()
        self.listen_connections()

    def init_server(self):
        try:
            print("Welcome Security Server")
            print(f"Max nodes to conect {self.settings.get_num_clients()}")
            self.socket.bind((self.host, self.port))
            self.socket.listen(self.settings.get_num_clients())
        except socket.error as e:
            print(str(e))
            
    def listen_connections(self):
        while True:
            conn, addr = self.socket.accept()
            connection = Connection(conn, addr)
            self.nodes.append(connection)
            self.nodes[self.nodes_i].start()
            self.nodes_i += 1
