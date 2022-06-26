import cv2
import time
from util.logger import print_log

def detector(connection):
    '''
    Method to a fire detection
    '''
    fire_cascade = cv2.CascadeClassifier('classifiers/fire_detection.xml')
    print_log('i', f"Fire detection on camera: { connection.cam_id }")
    while connection.running:
        time.sleep(0.1)
        frame = connection.get_frame()
        if frame is not None:
            fire = fire_cascade.detectMultiScale(frame, 1.2, 5)
            if len(fire) > 0:
                connection.fire_detections.append(frame)
    print_log('i', f"Finishing fire detection on camera: { connection.cam_id }")