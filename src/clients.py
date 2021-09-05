import socket
from loger import print_log
from threading import Thread

class Clients(Thread):
    
    def __init__(self, settings):
        Thread.__init__(self)
        
        self.settings = settings
        
        self.sckt_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = self.settings.get_host_address()
        self.port = self.settings.get_port_clients()
        
        self.clients_ready = False
        self.clients = []
    
    def stop_client_connections(self):
        for client in self.clients:
            client.do_run = False   
            client.join(1)
        
    def get_num_clients(self):
        return len(self.clients)
    
    def run(self):
        self.init_clients_thread()
        self.listen_clients_connection()
        # self.close_clients_connection()
        
    def init_clients_thread(self):
        print_log('i', 'Thread clients ready!')
        try:
            self.sckt_client.bind((self.host, self.port))
        except socket.error as e:
            print_log('w', f"Error init thread clients : {str(e)}")
        else:
            self.sckt_client.listen(self.settings.get_num_clients())
            self.clients_ready = True
    
    def listen_clients_connection(self):
        print_log('i', 'Listen clients...')
        while self.clients_ready:
            try:
                conn, addr = self.sckt_client.accept()
            except socket.error as e:
                print_log('w', f'Error on connect client : {str(e)}')
                self.clients_ready = False
            else:
                self.clients.append(Connection(conn, addr))
                self.clients[len(self.nodes)-1].start()
    
    def close_clients_connection(self):    
        if self.clients_ready:
            try:
                self.sckt_client.close()
            except socket.error as e:
                print_log(f'Error on Close Clients thread {str(e)}')
            else:
                self.stop_client_connections()
                print_log('i', 'Clients thread turned off')