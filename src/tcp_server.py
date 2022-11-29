from util.logger import print_log
from connection import Connection
from db_manager import create_database

import socket as skt
import settings as s
import uuid

host = s.get_host()
port = int(s.get_port())
database = None # global
stream_enabled = s.get_stream_enabled()
status_fire_detector = s.get_fire_detector_status()
status_motion_detector = s.get_motion_detector_status()
status_people_detector = s.get_people_detector_status()

class TCPServer:

    def __init__(self):
        """
        Method to init a TCPServer class from host and port.
        """ 
        self.socket = None 
        self.tcp_server_running = True
        self.connections = {} # to store every Connection object
        self.id_cameras = set()     # id cameras
        
    def prepare_server(self):
        """
        Method to prepare TCPServer from host and port to store connection object referencies.
        """
        try:
            global database
            print_log('i', "****** Welcome to the TCP-Server ******")
            database = create_database()
            self.socket = skt.socket(skt.AF_INET, skt.SOCK_STREAM)
            self.socket.bind((host, port))
            self.socket.listen(10)
            print_log('i', f"Serving on : {host}; on port : {port}")
            print_log('i', f"Streaming enabled : {stream_enabled}")
            print_log('i', f"Fire detector enabled : {status_fire_detector}")
            print_log('i', f"People detector enabled : {status_people_detector}")
            print_log('i', f"Motion detector enabled : {status_motion_detector}")
            
        except skt.error as e:
            print(str(e))
            
    def run(self):
        """
        Method to keep alive waiting to more connections.
        """
        global database
        print_log('i', "Listen connections : ")
        while self.tcp_server_running:
            try:
                connector, address = self.socket.accept()
                ident = uuid.uuid4()
                self.connections[ident] = Connection(ident, connector, address, database, self)
                self.connections[ident].start()
            except KeyboardInterrupt:
                self.tcp_server_running = False
                self.stop_all_connections()
                print_log('i', "Server turned-off from keyboard")
    
    def reg_connections(self, id_camera):
        """
        Log if a camera has not been connected prevoiusly.
        """
        self.id_cameras.add(id_camera)

    def is_connected(self, id_camera):
        """
        Check if id_camera is already in actual connections.
        """
        return id_camera in self.id_cameras

    def stop_all_connections(self):
        """
        Stop all connections that have been created.
        """
        for connection in self.connections.values():
            if connection.running:
                connection.stop_connection()
        print_log('i', "Stop all running connections")
    
    def print_number_of_connections(self):
        """
        Method to print logging number of connections.
        """
        cont=0
        for connection in self.connections.values():
            if connection.running:
                cont = cont + 1 
        print_log('i', f'Number of Connections : {cont}')

    def delete_id_camera(self, id_camera):
        """
        Method to delete id camera connection.
        """
        if id_camera in self.id_cameras:
            self.id_cameras.remove(id_camera)