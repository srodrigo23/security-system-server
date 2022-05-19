from threading import Thread

import sys
import struct
import pickle
import cv2

class FramesReceiver(Thread):
    """
    Frame thread receiver 
    """
    def __init__(self, connection):
        """
        Class constructor
        """ 
        Thread.__init__(self)
        self.data = b"" 
        self.payload_size = struct.calcsize(">L")
        self.__conn__ = connection
        self.__connect_ready__ = True
        self.__frame__ = None
        
    def run(self):
        """
        Method inherated to run a thread
        """
        while self.__connect_ready__:
            self.__frame__ = self.read_frame()

    def get_frame(self):
        return self.__frame__

    def get_message_size(self):
        """
        Method to get the frame size to build a frame again
        """
        while len(self.data) < self.payload_size and self.__connect_ready__:
            data = self.__conn__.recv(4096)
            if len(data) > 0:
                self.data += data
            else:
                self.stop_connection()
        if self.__connect_ready__:
            packed_msg_size = self.data[:self.payload_size] # receive image row data form client socket
            self.data = self.data[self.payload_size:]
            return struct.unpack(">L", packed_msg_size)[0]
        else:
            return 0
        
    def read_frame(self):
        """
        Method to read a frame
        """
        msg_size = self.get_message_size()
        if msg_size != 0:
            while len(self.data) < msg_size and self.__connect_ready__:
                data = self.__conn__.recv(4096)
                if len(data) > 0:
                    self.data += data
                else:
                    self.stop_connection()
            if self.__connect_ready__:
                frame_data = self.data[:msg_size]
                self.data = self.data[msg_size:]
                frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes") 
                return cv2.imdecode(frame, cv2.IMREAD_COLOR)
            else: 
                return None
        else:
            return None
        
    def stop_connection(self):
        """
        Method to stop frame receiver loop
        """
        self.__connect_ready__ = False