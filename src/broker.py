import cv2
from image_hub import ImageHub

image_hub = ImageHub()

while True:
    node_name, image = image_hub.recv_image()
    print(f"Frame recived {node_name}")
    
    cv2.imshow(node_name, image) #1 window for each  Camera

    image_hub.send_reply(b'OK')
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()