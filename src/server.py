from loger   import print_log
from clients import Clients
from nodes   import Nodes

import time

class Server():
    
    def __init__(self, settings):
        """
        To init server and give settings from settings.py
        """
        self.settings = settings    
        self.init_server()
        self.run()
            
    def init_server(self):
        """
        Launch nodes and clients
        """
        self.launch_clients(self.settings.get_host_address(), 
                            self.settings.get_port_clients(), 
                            self.settings.get_num_clients())
        
        self.launch_nodes(self.settings.get_host_address(),
                          self.settings.get_port_nodes(), 
                          self.settings.get_num_nodes())
        
    def launch_clients(self, host, port, num_clients):
        """
        Launch Client thread to listen (host, port) to all clients
        """
        self.clients_thread = Clients(host, port, num_clients)
        self.clients_thread.start()
    
    def launch_nodes(self, host, port, num_nodes):
        """
        Launch Nodes thread to listen frames from nodes in (host, port)
        """
        self.nodes_thread = Nodes(host, port, num_nodes)
        self.nodes_thread.start()
        
    def run(self):
        """
            Ruinning to let nodes and clients running
        """
        self.server_ready = True
        print_log('i', 'Server running...')
        try:
            while self.server_ready:     
                # to prevent cpu overcharge
                time.sleep(1) 
        except KeyboardInterrupt: # close all threads
            print('Server interrupted')
            print_log('e', 'Server interrupted...')
            self.stop_server()
            
    def stop_server(self):
        """
            Stop server in order to stop clients and nodes
        """
        self.server_ready = False
        self.stop_clients_thread()
        self.stop_nodes_thread()

    def stop_clients_thread(self):
        """
        Close clients connections and stop thread
        """
        print_log('i', 'Stopping all clients comunication...')
        self.clients_thread.running = False
        self.clients_thread.close_clients_connection()
        self.clients_thread.join(1)
    
    def stop_nodes_thread(self):
        """
        Close nodes connections and stop thread
        """
        print_log('i', 'Stopping all nodes comunication...')
        self.nodes_thread.running = False
        self.nodes_thread.close_nodes_connection()
        self.nodes_thread.join(1)
