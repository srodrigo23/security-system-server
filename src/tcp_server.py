
import socket as s
import struct
import zlib
import pickle
import cv2
import time
import sys

from util.logger import print_log
from PIL import Image, ImageOps
from threading import Thread

class TCPServer():
    """
    TCPServer class
    """
    def __init__(self, host, port):
        """
        Method to init a TCPServer class from host and port
        """
        self.__host__ = host
        self.__port__ = port
        self.__socket__ = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.setup_server()

    def setup_server(self):
        """
        Method to start a TCPServer form host and port and init __cons__ to store connection object referencies
        """
        try:
            self.__socket__.bind((self.__host__, self.__port__))
            self.__socket__.listen(10)
        except s.error as e:
            print(str(e))
        else:
            self.__cons__ = []  # to manage conections or a dictionary
            
    def run(self):
        """
        Method to keep alive waiting to more connections
        """
        print("Listen connections >")
        while True:
            conn, addr = self.__socket__.accept()
            self.start_new_connection(conn)
            # self.__cons__.append__((conn, addr))
            # self.show_server_info()

    def start_new_connection(self, conn):
        """
        Method to create a new connection from a camera in a new thread
        """
        thread = Thread(target=self.run_connection, args=(conn, ))
        thread.setDaemon(True)
        thread.start()

    def run_connection(self, connection):
        """
        Method to get frames every thread connection
        """
        data = b""
        payload_size = struct.calcsize(">L") # print("payload_size: {}".format(payload_size))
        while True:
            cabecera = 0
            while len(data) < payload_size:
                cabecera+=1
                data_received = connection.recv(4096) # critico
                if data_received == b"":
                    print('Operacion terminada')
                    break
                else:
                    data+=data_received
                    print(f'Recibiendo cabecera {cabecera}')
            #receive image row data from client socket
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            try:
                msg_size = struct.unpack(">L", packed_msg_size)[0]
            except struct.error as e:
                print(str(e))
                break
            while len(data) < msg_size:
                data_received = connection.recv(4096)
                if data_received == b"":
                    print('Operacion termanada')
                    break
                else:
                    data += data_received
            frame_data = data[:msg_size]
            data = data[msg_size:]     
            frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)  # Frame received
            print(str(frame))
            time.sleep(0.1)
        connection.close()
    
    def show_server_info(self):
        """
        Method to show server info
        """
        print(f'Num. conections : { len(self.cons) }')
        for conn in self.cons:
            print(f"Connection : {conn[1][0]} Address : {conn[1][1]}")