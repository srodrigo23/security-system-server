from logger import print_log
from threading import Thread
from connection import Connection
from _thread import start_new_thread

import socket
import time

class Node(Thread):
    
    def __init__(self, host, port, num_nodes):
        """
        Constructor of Nodes threads
        """
        Thread.__init__(self)
        self.host = host
        self.port = port
        print(f' node host {self.host} port {self.port}')
        self.num_nodes = num_nodes
        self.nodes_ready = False
        self.nodes = {}
        self.sckt_node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn = None
        
    def run(self):
        """
        Excecuton of thread 
        """
        self.bind_nodes()
        self.listen_nodes_connection()

    def bind_nodes(self):
        """
        Method to bind socket to listen node connections
        """
        print_log('i', "Thread nodes ready!")
        try:
            self.sckt_node.bind((self.host, self.port))
        except socket.error as e:
            print_log('w', f"Error init thread nodes : {str(e)}")
        else:
            self.sckt_node.listen(self.num_nodes)
            self.nodes_ready = True
    
    def listen_nodes_connection(self):
        """
        Method to accept nodes to connection
        """
        print_log('i', 'Listen nodes...')
        while self.nodes_ready:
            try:
                self.conn, addr = self.sckt_node.accept()
            except socket.error as e:
                print_log('w', f'Error on connect node : {str(e)}')
                self.nodes_ready = False
            else:
                print("Node connected")
                print(f" {addr[0]}  {addr[1]}")
                start_new_thread(self.send_messages,())
                # pass
                # registering thread connection
                # self.nodes.append(Connection(
                #     self.get_num_nodes(), conn, addr))
                # self.nodes[len(self.nodes)-1].start()
                
    def send_messages(self):
        self.conn.sendall(b'send')
        while True:
            data = self.conn.recv(1024)
            print(data)
            time.sleep(1)

    def close_nodes_connection(self):
        """
        Close connections and stop nodes connections
        """
        if self.nodes_ready:
            try:
                self.sckt_node.close()
            except socket.error as e:
                print_log('w', f'Error on Close Nodes thread {str(e)}')
            else:
                self.stop_node_connections()
                print_log('i', 'Nodes thread turned off')

    def stop_node_connections(self):
        """
        Stop all node threads in order to close connections
        """
        pass
        # for node in self.nodes:
        #     node.do_run = False
        #     node.join(1)

    def get_num_nodes(self):
        """
        Method to get number of nodes
        """
        return len(self.nodes)
