"""
Author  : Sergio Rodrigo Cardenas Rivera
Email   : rodrigosergio93@gmail.com
Version : 1.0
GitHub  : @srodrigo23
"""
from threading import Thread
import time
import cv2
from util.logger import print_log

# import numpy as np
# Fire_Reported = 0

class FireDetector(Thread):
    """
    Fire detection
    """

    def __init__(self, connection) -> None:
        Thread.__init__(self)
        self.running = False
        self.connection = connection
        self.objetive = 'fire_detector'

    def run(self) -> None:
        """
        Method to a fire detection
        """
        fire_cascade = cv2.CascadeClassifier(
            'detectors/fire_detection.xml'
        )
        print_log('i', f"Fire detection on camera: { self.connection.cam_id }")
        time.sleep(2)
        self.running = True
        while self.running:
            time.sleep(0.1)
            frame, label = self.connection.get_frame(objetive='fire_detector')
            if frame is not None:
                # fire = fire_cascade.detectMultiScale(frame, 12, 5)
                fire = fire_cascade.detectMultiScale(
                    image=frame,
                    scaleFactor=1.1,
                    minNeighbors=3,
                    flags=0
                )
                
                if len(fire) > 0:
                    for (_x_,_y_,_w_,_h_) in fire:
                        cv2.rectangle(
                            frame,
                            (_x_-20,_y_-20),
                            (_x_+_w_+20,_y_+_h_+20),
                            (0,255,0),
                            2
                        )
                    print_log('i', f"Fire detected: { self.connection.cam_id }")
                    self.connection.fire_detections.append((frame, label))
        print_log('i', f"Finishing fire detection on camera: { self.connection.cam_id }")
    
    def stop(self) -> None:
        """
        Stop fire detector thread
        """
        self.running = False
        

# def detector(connection):
#     """
#     Method to a fire detection
#     """
#     fire_cascade = cv2.CascadeClassifier(
#         'detectors/fire_detection.xml'
#     )
#     print_log('i', f"Fire detection on camera: { connection.cam_id }")
#     time.sleep(2)
    
#     while connection.running:
#         time.sleep(0.1)
#         frame, label = connection.get_frame(objetive='fire_detector')
#         if frame is not None:
#             # fire = fire_cascade.detectMultiScale(frame, 12, 5)
#             fire = fire_cascade.detectMultiScale(
#                 image=frame,
#                 scaleFactor=1.1,
#                 minNeighbors=3,
#                 flags=0
#             )
            
#             if len(fire) > 0:
#                 for (_x_,_y_,_w_,_h_) in fire:
#                     cv2.rectangle(
#                         frame,
#                         (_x_-20,_y_-20),
#                         (_x_+_w_+20,_y_+_h_+20),
#                         (0,255,0),
#                         2
#                     )
#                 print_log('i', f"Fire detected: { connection.cam_id }")
#                 connection.fire_detections.append((frame, label))
#     print_log('i', f"Finishing fire detection on camera: { connection.cam_id }")
    

    # # video = cv2.VideoCapture("video_file") # If you want to use webcam use Index like 0,1.
    # Fire_Reported = 0
    # while connection.running:
    #     frame, label = connection.get_frame(objetive='fire_detector')
        
    #     frame = cv2.resize(frame, (960, 540))

    #     blur = cv2.GaussianBlur(frame, (21, 21), 0)
    #     hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    #     lower = [18, 50, 50]
    #     upper = [35, 255, 255]
    #     lower = np.array(lower, dtype="uint8")
    #     upper = np.array(upper, dtype="uint8")

    #     mask = cv2.inRange(hsv, lower, upper)

    #     output = cv2.bitwise_and(frame, hsv, mask=mask)

    #     no_red = cv2.countNonZero(mask)

    #     if int(no_red) > 15000:
    #         Fire_Reported = Fire_Reported + 1
    #         connection.fire_detections.append((frame, label))

    #     # cv2.imshow("output", output)

    #     # if Fire_Reported >= 1:

    #         # if Alarm_Status == False:
    #         #     threading.Thread(target=play_alarm_sound_function).start()
    #         #     Alarm_Status = True

    #         # if Email_Status == False:
    #         #     threading.Thread(target=send_mail_function).start()
    #         #     Email_Status = True