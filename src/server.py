import cv2
import socket
import logging
from settings import Settings

# from image_hub import ImageHub

class Server():
    
    def __init__(self)
        self.settings = Settings()
        self.socket = socket.socket(s.AF_INET, s.SOCK_STREAM)
        self.host = settings.get_host()
        self.port = settings.get_port()
        
        self.nodes = [] # to manage conections
        self.clients = []
        self.nodes_i = 0
        
        self.init_server()
        self.listen_connections()

    def init_server(self):
        try:
            self.socket.bind((self.host, self.port))
            self.socket.listen(settings.get_num_clients())
        except socket.error as e:
            print(str(e))
            
    def listen_connections():
        while True:
            conn, addr = self.socket.accept()
            connection = Connection(conn, addr)
            self.nodes.append(connection)
            self.nodes[nodes_i].start()
            nodes_i += 1

image_hub = ImageHub()
while True:
    node_name, image = image_hub.recv_image()
    print(f"Frame recived {node_name}")
    
    cv2.imshow(node_name, image) #1 window for each  Camera

    image_hub.send_reply(b'OK')
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()