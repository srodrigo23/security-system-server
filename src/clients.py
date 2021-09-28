from loger import print_log
from threading import Thread

import socket

class Clients(Thread):
    
    def __init__(self, host, port, num_clients):
        """
        Constructor of Clients threads
        """
        Thread.__init__(self)
        self.host = host
        self.port = port
        print(f' client host {self.host} port {self.port}')
        self.num_clients = num_clients
        self.clients_ready = False
        self.clients = {} # dictionary to store id and frames
        self.sckt_client = socket.socket(socket.AF_INET, 
                                         socket.SOCK_STREAM)
    
    def run(self):
        """
        Excecuton of thread 
        """
        self.bind_clients()
        self.listen_clients_connection()
        
    def bind_clients(self):
        """
        Method to bind socket to listen client connections
        """
        print_log('i', 'Thread clients ready!')
        try:
            self.sckt_client.bind((self.host, self.port))
        except socket.error as e:
            print_log('w', f"Error init thread clients : {str(e)}")
        else:
            self.sckt_client.listen(self.num_clients)
            self.clients_ready = True
    
    def listen_clients_connection(self):
        """
        Method to accept clients to connection
        """
        print_log('i', 'Listen clients...')
        while self.clients_ready:
            try:
                conn, addr = self.sckt_client.accept()
            except socket.error as e:
                print_log('w', f'Error on connect client : {str(e)}')
                self.clients_ready = False
            else:
                pass
                # registering thread connection
                # self.clients.append(Connection(conn, addr))
                # self.clients[len(self.nodes)-1].start()
    
    def close_clients_connection(self):
        """
        Close connections and stop clients connections
        """
        if self.clients_ready:
            try:
                self.sckt_client.close()
            except socket.error as e:
                print_log(f'Error on Close Clients thread {str(e)}')
            else:
                self.stop_client_connections()
                print_log('i', 'Clients thread turned off')

    def stop_client_connections(self):
        """
        Stop all client threads in order to close connections
        """
        pass
        # for client in self.clients:
        #     client.do_run = False
        #     client.join(1)

    def get_num_clients(self):
        """
        Method to get number of clients
        """
        return len(self.clients)
