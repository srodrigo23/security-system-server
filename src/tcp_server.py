from logger   import print_log

import socket
import struct  # new

import numpy as np
import struct  # new
import zlib
import pickle
from PIL import Image, ImageOps
import cv2

from threading import Thread
import socket as s
import time
import sys
import time

class TCPServer():
    def __init__(self, host, port):
        self.__host__ = host
        self.__port__ = port
        self.__socket__ = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.setup_server()

    def setup_server(self):
        try:
            self.__socket__.bind((self.__host__, self.__port__))
            self.__socket__.listen(10)
        except s.error as e:
            print(str(e))
        else:
            self.__cons__ = []  # to manage conections
            
    def run(self):
        print("Listen connections >")
        while True:
            conn, addr = self.__socket__.accept()
            self.start_new_connection(conn)
            # self.__cons__.append__((conn, addr))
            # self.show_server_info()

    def start_new_connection(self, conn):
        thread = Thread(target=self.run_connection, args=(conn, ))
        thread.setDaemon(True)
        thread.start()

    def run_connection(self, connection):
        # connection.send(str.encode('Welcome to the Server'))
        print("New Connection")
        """
        New Connection listening frames
        """
        data = b""
        payload_size = struct.calcsize(">L")
        print("payload_size: {}".format(payload_size))
        cabecera = 0
        
        while True:
            while len(data) < payload_size:
                cabecera+=1
                data_received = connection.recv(4096) # critico
                if data_received == b"":
                    print('Operacion termanada')
                    break
                else:
                    data+=data_received
                    print(f'recibiendo cabecera {cabecera}')
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
            
            # data = connection.recv(2048)
            # entry = data.decode('utf-8')
            # print(entry)
            # reply = 'Server says ' + data.decode('utf-8')
            # if not data:
            #     break
            # connection.sendall(str.encode(reply))
        connection.close()
    
    def show_server_info(self):
        # TODO Some strucutures dont implemented
        print(f'Num. conections : { len(self.cons) }')
        for con in self.cons:
            print(f"Connection : {con[1][0]} Address : {con[1][1]}")


def run_tcp_server(host, port):
    TCPServer(host, port).run()

if __name__ == "__main__":
    host = sys.argv[1]
    port = sys.argv[2]
    run_tcp_server(host, int(port))
