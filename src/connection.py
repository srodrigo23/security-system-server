import sys
import struct
import cv2
import pickle

from threading import Thread
import logger
if sys.version_info >= (3, 0):
    from queue import Queue
else:
    from Queue import Queue

class Connection(Thread):
    
    def __init__(self, ident, client, address):
        """
        Method to create a connection from 
        """
        Thread.__init__(self)
        self.id = ident # identificador HASH
        self.client = client
        self.address = address
        self.data = b""        
        self.payload_size = struct.calcsize(">L")
        self.connect_ready = True
        
        self.frames_queue = Queue(maxsize=128)
        
    def run(self):
        while self.connect_ready:
            frame = self.read_frame()
            # self.frames_queue.put(frame)

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
            self.data += self.client.recv(4096)
        packed_msg_size = self.data[:self.payload_size] # receive image row data form client socket
        self.data = self.data[self.payload_size:]
        return struct.unpack(">L", packed_msg_size)[0]  

    def read_frame(self):
        """
        Method to read a frame
        """
        msg_size = self.get_message_size()
        print(f"node {self.id} {msg_size}")
        while len(self.data) < msg_size:
            self.data += self.client.recv(4096)
        frame_data = self.data[:msg_size]
        self.data = self.data[msg_size:]
        frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes") # unpack image using pickle 
        return  cv2.imdecode(frame, cv2.IMREAD_COLOR)
    
    def stop_connection(self):
        """
        
        """
        self.connect_ready = False