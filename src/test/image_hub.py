import zmq
import numpy as np

from serializing import SerializingContext

class ImageHub():
    
    def __init__(self, open_port='tcp://*:5555', REQ_REP = True):
        self.REQ_REP = REQ_REP
        if REQ_REP==True:
            #Init REP socket for blocking mode
            self.init_reqrep(open_port)
        else:
            #Connect to PUB socket for non-blocking mode
            self.init_pubsub(open_port)

    def init_reqrep(self, address): 
        # Initializes Hub in REQ/REP mode
        socketType = zmq.REP
        self.zmq_context = SerializingContext()
        self.zmq_socket = self.zmq_context.socket(socketType)
        self.zmq_socket.bind(address)

    def init_pubsub(self, address):
        # Initialize Hub in PUB/SUB mode
        socketType = zmq.SUB
        self.zmq_context = SerializingContext()
        self.zmq_socket = self.zmq_context.socket(socketType)
        self.zmq_socket.setsockopt(zmq.SUBSCRIBE, b'')
        self.zmq_socket.connect(address)
       
    def connect(self, open_port):    
        if self.REQ_REP == False:
            #This makes sense only in PUB/SUB mode
            self.zmq_socket.setsockopt(zmq.SUBSCRIBE, b'')
            self.zmq_socket.connect(open_port)
            self.zmq_socket.subscribe(b'')
        return

    def recv_image(self, copy=False):    
        msg, image = self.zmq_socket.recv_array(copy=False)
        return msg, image

    def recv_jpg(self, copy=False):
        msg, jpg_buffer = self.zmq_socket.recv_jpg(copy=False)
        return msg, jpg_buffer

    def send_reply(self, reply_message=b'OK'):        
        self.zmq_socket.send(reply_message)

    def close(self):
        # Closes the ZMQ socket and the ZMQ context.
        self.zmq_socket.close()
        self.zmq_context.term()

    def __enter__(self):
        # Enables use of ImageHub in with statement. Returns: self.
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        #Enables use of ImageHub in with statement.
        self.close()