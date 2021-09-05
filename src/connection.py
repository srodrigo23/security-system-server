import sys
import struct
import cv2
import pickle

from threading import Thread
import loger
if sys.version_info >= (3, 0):
    from queue import Queue
else:
    from Queue import Queue

class Connection(Thread):
    
    def __init__(self, ident,  client, address):
        Thread.__init__(self)
        
        self.id = ident # indetificador
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
    
    """
    To return the frame recieved from node to be readed by a client.
    """
    def get_frame(self):
        return self.frames_queue.get()
    
    """
    To get the frame size
    """
    def get_message_size(self):
        while len(self.data) < self.payload_size:
            self.data += self.client.recv(4096)
        packed_msg_size = self.data[:self.payload_size] # receive image row data form client socket
        self.data = self.data[self.payload_size:]
        return struct.unpack(">L", packed_msg_size)[0]  

    def read_frame(self):
        msg_size = self.get_message_size()
        print(f"node {self.id} {msg_size}")
        while len(self.data) < msg_size:
            self.data += self.client.recv(4096)
        frame_data = self.data[:msg_size]
        self.data = self.data[msg_size:]
        frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes") # unpack image using pickle 
        return  cv2.imdecode(frame, cv2.IMREAD_COLOR)
    
    def stop_connection(self):
        self.connect_ready = False
        
