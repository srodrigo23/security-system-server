from util.logger import print_log
from connection import Connection

import socket as s
import uuid

class TCPServer():
    """ TCPServer class """
    def __init__(self, host, port):
        """ Method to init a TCPServer class from host and port """
        self.__socket__ = None
        self.__host__ = host
        self.__port__ = port
        self.__connections__ = {}       # to store every Connection object
        self.__tcp_server_ready__ = True
        self.__id_cameras__ = set()     # id cameras
        
    def prepare_server(self):
        """ Method to prepare TCPServer from host and port to store connection object referencies """
        try:
            self.__socket__ = s.socket(s.AF_INET, s.SOCK_STREAM)
            self.__socket__.bind((self.__host__, self.__port__))
            self.__socket__.listen(10)
            print_log('i', f"Serving on : {self.__host__}; on port : {self.__port__}")
        except s.error as e:
            print(str(e))
            
    def run(self):
        """ Method to keep alive waiting to more connections """
        print_log('i', "Listen connections : ")
        while self.__tcp_server_ready__:
            try:
                connector, address = self.__socket__.accept()
                ident = uuid.uuid4()
                new_connection = Connection(
                    id_uuid4=ident,
                    connector=connector,
                    address=address,
                    tcp_server=self)
                self.__connections__[ident] = new_connection
                self.__connections__[ident].start()
            except KeyboardInterrupt:
                self.__tcp_server_ready__ = False
                self.stop_all_connections()
                print_log('i', "Server turned-off from keyboard")
    
    def reg_connections(self, id_camera):
        """ Log if a camera has not been connected prevoiusly """
        self.__id_cameras__.add(id_camera)

    def is_camera_connected(self, id_camera):
        """ Check if id_camera is already in actual connections """
        return  id_camera in self.__id_cameras__

    def stop_all_connections(self):
        """ Stop all connections that have been created """
        for connection in self.__connections__.values():
            if connection.__running__:
                connection.stop_connection()
        print_log('i', "Stop all running connections")
    
    def print_number_of_connections(self):
        """ Method to print logging number of connections """
        cont=0
        for connection in self.__connections__.values():
            if connection.__running__:
                cont = cont + 1 
        print_log('i', f'Number of Connections : {cont}')

    def delete_id_camera(self, id_camera):
        """ Method to delete id camera connection """
        if id_camera in self.__id_cameras__:
            self.__id_cameras__.remove(id_camera)