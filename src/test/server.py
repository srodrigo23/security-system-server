image_hub = ImageHub()
while True:
    node_name, image = image_hub.recv_image()
    print(f"Frame recived {node_name}")

    cv2.imshow(node_name, image)  # 1 window for each  Camera

    image_hub.send_reply(b'OK')

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()


"""
Method to review if a socket port is used
"""
def prepare(self):
    if is_host_port_in_use(self.host, self.port):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

def is_host_port_in_use(host, port):
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, port)) == 0