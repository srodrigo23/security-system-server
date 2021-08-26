import struct
import logging
import cv2

from threading import Thread

class Connection(Thread):
    
    def __init__(self, client, address):
        Thread.__init__(self)
        self.client = client
        self.address = address
        self.data = b""        
        self.payload_size = struct.calcsize(">L")
        
        logging.info(f"payload_size: { self.payload_size }")
        
    def run(self):
        while True:
            frame = read_frame()
            cv2.imshow('server',frame)
            cv2.waitKey(1)
    
    def get_message_size(self):
        while len(self.data) < self.payload_size:
            self.data += self.client.recv(4096)
        packed_msg_size = self.data[:self.payload_size] # receive image row data form client socket
        self.data = self.data[self.payload_size:]
        return struct.unpack(">L", packed_msg_size)[0]  

    def read_frame(self):
        msg_size = self.get_message_size()
        while len(self.data) < msg_size:
            self.data += self.client.recv(4096)
        frame_data = self.data[:msg_size]
        self.data = self.data[msg_size:]
        frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes") # unpack image using pickle 
        return  cv2.imdecode(frame, cv2.IMREAD_COLOR)