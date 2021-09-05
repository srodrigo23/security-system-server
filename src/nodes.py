import socket
from loger import print_log
from threading import Thread
from connection import Connection

class Nodes(Thread):
    
    def __init__(self, settings):
        Thread.__init__(self)
        self.settings = settings
        self.sckt_node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = self.settings.get_host_address()
        self.port = self.settings.get_port_nodes()
        self.nodes_ready = False
        self.nodes = []

    def stop_node_connections(self):
        for node in self.nodes:
            node.do_run = False
            node.join(1)

    def get_num_nodes(self):
        return len(self.nodes)
    
    def run(self):
        self.init_nodes_thread()
        self.listen_nodes_connection()
        # self.close_nodes_connection()

    def init_nodes_thread(self):
        print_log('i', "Thread nodes ready!")
        try:
            self.sckt_node.bind((self.host, self.port))
        except socket.error as e:
            print_log('w', f"Error init thread nodes : {str(e)}")
        else:
            self.sckt_node.listen(self.settings.get_num_nodes())
            self.nodes_ready = True
    
    def listen_nodes_connection(self):
        print_log('i', 'Listen nodes...')
        while self.nodes_ready:
            try:
                conn, addr = self.sckt_node.accept()
            except socket.error as e:
                print_log('w', f'Error on connect node : {str(e)}')
                self.nodes_ready = False
            else:
                print('connection')
                self.nodes.append(Connection(self.get_num_nodes(), conn, addr))
                self.nodes[len(self.nodes)-1].start()

    def close_nodes_connection(self):
        if self.nodes_ready:
            try:
                self.sckt_node.close()
            except socket.error as e:
                print_log('w', f'Error on Close Nodes thread {str(e)}')
            else:
                self.stop_node_connections()
                print_log('i', 'Nodes thread turned off')