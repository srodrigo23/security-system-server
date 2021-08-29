import socket
from threading import Thread


class Clients(Thread):
    
    def __init__(self, settings):
        Thread.__init__(self)
        self.settings = settings
        self.sckt_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = self.settings.get_host_address()
        self.port = self.settings.get_port_clients()
        self.clients_ready = True
        self.clients = []
        
    def get_num_clients(self):
        return len(self.clients)
    
    def run(self):
        self.init_clients_thread()
        self.listen_clients_connection()
        self.close_clients_connection()
        
    def init_clients_thread(self):
        print("Thread clients ready!")
        try:
            self.sckt_client.bind((self.host, self.port))
            self.sckt_client.listen(self.settings.get_num_clients())
            self.clients_ready = True
        except socket.error as e:
            print(f"Error init clients : {str(e)}")
    
    def listen_clients_connection(self):
        print('Listen clients...')
        while self.clients_ready:
            try:
                conn, addr = self.sckt_client.accept()
                # self.nodes.append(Connection(conn, addr))
                # self.nodes[len(self.nodes)-1].start()
            except socket.error as e:
                self.clients_ready = False
                print(f'Error on Listen client connection : {str(e)}')
    
    def close_clients_connection(self):
        print('Clients thread turned off')
        try:
            self.sckt_client.close()
        except socket.error as e:
            print(f'Error on Close Clients thread {str(e)}')
    
