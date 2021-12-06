import sys
import struct
import cv2
import pickle

from util.logger import print_log
from util.date import get_current_time_string
from live_streaming import LiveStreaming

class Connection:
    
    def __init__(self, ident, connection, address, id_random_gen, fb_admin):
        """
        Method to create a connection from 
        """
        self.conn = connection
        self.data = b"" # ???????
        self.payload_size = struct.calcsize(">L")
        
        self.__frame__ = None
        
        self.__uuid__ = ident
        self.__id_random_generator__ = id_random_gen
        self.__id__ = self.__id_random_generator__.get_new_code()
        self.__connect_ready__ = True
        self.__fb_admin__ = fb_admin
        self.__addr__ = address
        
        self.__live_streaming__ = LiveStreaming(self, 'path', 'hls', 25)
        
    def run(self):
        """
        Method to read frames from camera
        """
        print_log('i', f"New Connection : {self.__addr__}")
        self.__fb_admin__.record_connection(self.__id__, self.__uuid__, get_current_time_string(), self.__addr__, True)
        while self.__connect_ready__:
            frame = self.read_frame() # dictionary of frames
            # print(type(frame))
            if frame is not None:
                self.__frame__ = frame
            else:
                self.__connect_ready__ = False
        self.conn.close()
        print_log('i', "Connection Closed")
        self.__fb_admin__.record_connection(self.__id__, self.__uuid__, get_current_time_string(), self.__addr__, False)

    def get_frame(self):
        """
        To return the frame recieved from node to be readed by a client.
        """
        return self.__frame__
    
    def get_message_size(self):
        """
        To get the frame size
        """
        while len(self.data) < self.payload_size and self.__connect_ready__:
            data = self.conn.recv(4096)
            if len(data) > 0:
                self.data += data
            else:
                self.__connect_ready__ = False
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
                data = self.conn.recv(4096)
                if len(data) > 0:
                    self.data += data
                else:
                    self.__connect_ready__ = False
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
        Method to stop connection
        """
        self.__connect_ready__ = False