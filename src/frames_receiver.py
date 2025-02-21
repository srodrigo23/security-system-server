"""
Author  : Sergio Rodrigo Cardenas Rivera
Email   : rodrigosergio93@gmail.com
Version : 1.0
GitHub  : @srodrigo23
"""

from threading import Thread
import struct
import pickle
import socket as skt
import cv2

class FramesReceiver(Thread):
    """
    Class to receive frames from socket connection
    """
    def __init__(self, connection):
        Thread.__init__(self)
        self.data = b""
        self.payload_size = struct.calcsize(">L")
        self.conn = connection
        self.running = True
        self.frame = None
        
    def run(self):
        """
        Method inherated to run a thread.
        """
        while self.running:
            self.frame = self.read_frame()

    def get_frame(self):
        """
        Method to return frame received.
        """
        return self.frame

    def get_message_size(self):
        """
        Method to get the frame size to build a frame again.
        """
        while len(self.data) < self.payload_size and self.running:
            try:
                data = self.conn.recv(4096)
                if len(data) > 0:
                    self.data += data
                else:
                    self.stop_connection()
            except skt.error as error:
                print(f"{error} error in get message size")
                self.stop_connection()
            except KeyboardInterrupt:
                print('i', "Error getting images")
        if self.running:
            packed_msg_size = self.data[:self.payload_size] # receive image row data form client socket
            self.data = self.data[self.payload_size:]
            return struct.unpack(">L", packed_msg_size)[0]
        else:
            return 0
        
    def read_frame(self):
        """
        Method to read a frame.
        """
        msg_size = self.get_message_size()
        if msg_size != 0:
            try:
                while len(self.data) < msg_size and self.running:
                    try:
                        data = self.conn.recv(4096)
                        if len(data) > 0:
                            self.data += data
                        else:
                            self.stop_connection()
                    except Exception as e:
                        print(f"{e} error in read frame")
                        self.stop_connection()
                if self.running:
                    frame_data = self.data[:msg_size]
                    self.data = self.data[msg_size:]
                    frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
                    return cv2.imdecode(frame, cv2.IMREAD_COLOR)
                else:
                    print("Returning none")
                    return None
            except KeyboardInterrupt:
                print("there was an error")
        else:
            return None
        
    def stop_connection(self):
        """
        Method to stop frame receiver loop.
        """
        self.running = False
        