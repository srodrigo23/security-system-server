from threading import Thread

class FramesReceiver(Thread):
    
    def __init__(self):
        Thread.__init__(self)
        
        self.data = b"" 
        self.payload_size = struct.calcsize(">L")
        
        
    def run(self):
        
    
    
    def get_message_size(self):
        """
        To get the frame size
        """
        while len(self.data) < self.payload_size and self.__connect_ready__:
            data = self.conn.recv(4096)
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
                data = self.conn.recv(4096)
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
        
    