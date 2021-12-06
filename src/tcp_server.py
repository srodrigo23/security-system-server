
import socket as s
import struct
import zlib
import pickle
import cv2
import time
import sys
import uuid
from connection import Connection

from util.logger import print_log
from PIL import Image, ImageOps
from threading import Thread
from connection import Connection
from util.random_code import RandomCode
from database.firebase_manager import FirebaseManager

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
        self.__connections__ = {} #to store every Connection object
        
        self.__id_generator__ = RandomCode(1, 20) #Code generator 1-20
        self.__firebase_manager__ = FirebaseManager() # Firebase manager
        # self.__frames_from_every_conn__ = {} # to store every frame
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
            
    def run(self):
        """
        Method to keep alive waiting to more connections
        """
        print_log('i', "Listen connections : ")
        while True:
            try:
                conn, addr = self.__socket__.accept()
                ident = uuid.uuid4() 
                self.start_new_connection(ident, conn, addr, self.__id_generator__, self.__firebase_manager__)
            except KeyboardInterrupt:
                print_log('i', "Server turned-off from keyboard")
                break

    def start_new_connection(self, ident, conn, addr, id_generator, fb_manager):
        """
        Method to create a new connection from a camera in a new thread
        """
        conn = Connection(ident, conn, addr, id_generator, fb_manager)
        self.__connections__[ident] = Thread(target=conn.run, args=())
        self.__connections__[ident].setDaemon(True)
        self.__connections__[ident].start()
    
    