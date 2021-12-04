import sys
import struct
import cv2
import pickle

from util.logger import print_log

class Connection:
    
    def __init__(self, ident, connection, address, frames):
        """
        Method to create a connection from 
        """
        self.id = ident
        self.conn = connection
        self.addr = address
        self.data = b"" # ???????
        self.payload_size = struct.calcsize(">L")
        self.frame = None
        self.connect_ready = True
        self.frames = frames # frames dictionary
        
    def run(self):
        """
        Method to read frames from camera
        """
        print_log('i', f"New Connection {self.id} - {self.addr}")
        while self.connect_ready:
            self.frames[self.id] = self.read_frame() # dictionary of frames
        self.conn.close()
        print_log('i', "")

    def get_frame(self):
        """
        To return the frame recieved from node to be readed by a client.
        """
        return self.frames_queue.get()
    
    def get_message_size(self):
        """
        To get the frame size
        """
        while len(self.data) < self.payload_size:
            self.data += self.conn.recv(4096)
        packed_msg_size = self.data[:self.payload_size] # receive image row data form client socket
        self.data = self.data[self.payload_size:]
        return struct.unpack(">L", packed_msg_size)[0]  

    def read_frame(self):
        """
        Method to read a frame
        """
        msg_size = self.get_message_size()
        while len(self.data) < msg_size:
            self.data += self.conn.recv(4096)
        frame_data = self.data[:msg_size]
        self.data = self.data[msg_size:]
        frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes") 
        return  cv2.imdecode(frame, cv2.IMREAD_COLOR)
    
    def stop_connection(self):
        """
        Method to stop connection
        """
        self.connect_ready = False