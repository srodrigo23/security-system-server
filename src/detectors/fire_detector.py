"""
Methods to detect fire
"""
import time
import cv2
from util.logger import print_log

def detector(connection):
    """
    Method to a fire detection
    """
    fire_cascade = cv2.CascadeClassifier(
        'classifiers/fire_detection.xml'
    )
    print_log('i', f"Fire detection on camera: { connection.cam_id }")
    while connection.running:
        time.sleep(0.1)
        frame, label = connection.get_frame(objetive='fire_detector')
        if frame is not None:
            fire = fire_cascade.detectMultiScale(frame, 1.2, 5)
            for (_x_,_y_,_w_,_h_) in fire:
                cv2.rectangle(
                    frame,
                    (_x_-20,_y_-20),
                    (_x_+_w_+20,_y_+_h_+20),
                    (255,0,0),
                    2
                )
            if len(fire) > 0:
                connection.fire_detections.append((frame, label))
    print_log('i', f"Finishing fire detection on camera: { connection.cam_id }")
    