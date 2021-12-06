
import cv2
import time


class FireDetector(Thread):
    
    def __init__(self, connection):
        
        self.fire_cascade = cv2.CascadeClassifier('fire_detection.xml')
        self.connection = connection

    def run(self):        
        while True:
            frame = self.connection.get_fire_detector_frame()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            fire = fire_cascade.detectMultiScale(frame, 1.2, 5)

            for (x,y,w,h) in fire:
                cv2.rectangle(frame,(x-20,y-20),(x+w+20,y+h+20),(255,0,0),2)
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = frame[y:y+h, x:x+w]
