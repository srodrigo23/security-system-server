from util.logger import print_log
from connection import Connection
from util.id_generator import IDGenerator

import socket as s
import uuid

class TCPServer():
    """
    TCPServer class
    """
    def __init__(self, host, port):
        """
        Method to init a TCPServer class from host and port
        """
        self.__socket__ = None
        self.__host__ = host
        self.__port__ = port
        self.__connections__ = {} #to store every Connection object        
        self.__id_gen__ = IDGenerator() #ID consecitive generator
        self.__tcp_server_ready__ = True
        
    def prepare_server(self):
        """
        Method to prepare TCPServer from host and port to store connection object referencies
        """
        try:
            self.__socket__ = s.socket(s.AF_INET, s.SOCK_STREAM)
            self.__socket__.bind((self.__host__, self.__port__))
            self.__socket__.listen(10)
            print_log('i', f"Serving on : {self.__host__}; on port : {self.__port__}")
        except s.error as e:
            print(str(e))
            
    def run(self):
        """
        Method to keep alive waiting to more connections
        """
        print_log('i', "Listen connections : ")
        while self.__tcp_server_ready__:
            try:
                connector, address = self.__socket__.accept()
                ident = uuid.uuid4()
                self.__connections__[ident] = Connection(id_con = self.__id_gen__.get_generate_id(),
                                                         id_uuid4 = ident,
                                                         connector = connector, 
                                                         address = address)
                self.__connections__[ident].start()            
            except KeyboardInterrupt:
                self.__tcp_server_ready__ = False
                self.stop_all_connections()
                print_log('i', "Server turned-off from keyboard")
    
    def stop_all_connections(self):
        """
        Stop all connections that have been created
        """
        for key in self.__connections__:
            self.__connections__[key].stop_connection()
        print_log('i', "Stop all connections")