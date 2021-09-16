from threading import Thread
from _thread import start_new_thread

class ClientConnection(Thread):
    
    def __init__(self, connection, client, address):
        Thread.__init__(self)
        self.conn = connection
            
    def send_message(self, order):
        if order=='clock':
            
    
    
    def run(self):
        while True:
            message = self.conn.recv(1024)
            if message == 'clock':
                    
        
        