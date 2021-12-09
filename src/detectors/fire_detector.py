
import cv2
import time

from threading import Thread
from util.logger import print_log

class FireDetector(Thread):
    
    def __init__(self, connection, fb_admin):
        """
        Method to initialize Fire detector
        """
        Thread.__init__(self)
        self.__fire_cascade__ = cv2.CascadeClassifier('fire_detection.xml')
        self.__connection__ = connection
        self.__fb_admin__ = fb_admin
        
        self.__detector_ready__ = True
        self.__frame__ = None

    def run(self):
        """
        Method to execute detector
        """
        while self.__detector_ready__:
            time.sleep(0.1) # to prevent overcharge cpu
            self.__frame__ = self.__connection__.get_frame_to_fire_detector()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            fire = self.__fire_cascade__.detectMultiScale(self.__frame__, 1.2, 5)
            if len(fire) > 0:
                """
                to notify fire
                """
                pass
            for (x,y,w,h) in fire:
                cv2.rectangle(self.__frame__,(x-20,y-20),(x+w+20,y+h+20),(255,0,0),2)
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = frame[y:y+h, x:x+w]