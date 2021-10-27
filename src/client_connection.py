from threading import Thread

class ClientConnection(Thread):
    
    def __init__(self, connection, client, address):
        Thread.__init__(self)
        self.conn = connection
            
    def send_message(self, order):
        if order=='clock':
            pass
        
    def run(self):
        while True:
            message = self.conn.recv(1024)
            if message == 'clock':
    