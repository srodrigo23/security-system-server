"""
Motion detection
"""
import time
import cv2
from util.logger import print_log

def detector(connection):
    """
    Method to motion detection
    """
    static_back = None
    print_log('i', f"Motion detection on camera: { connection.cam_id }")
    time.sleep(2)
    while connection.running:
        time.sleep(0.1)
        frame, label = connection.get_frame(objetive='motion_detector')
        if frame is not None:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)
            if static_back is None:
                static_back = gray
                continue
            diff_frame = cv2.absdiff(static_back, gray)
            # If change in between static background and current frame is
            # grather than 30 it will show white color(255)
            thresh_frame = cv2.threshold(diff_frame, 30, 255, cv2.THRESH_BINARY)[1]
            thresh_frame = cv2.dilate(thresh_frame, None, iterations=3)
            # Finding contour of moving object
            cnts, _ = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for contour in cnts:
                if cv2.contourArea(contour) < 1000: continue
                (x, y, w, h) = cv2.boundingRect(contour)
                # making green rectangle arround the moving object
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 1)
            if len(cnts) > 0:
                print_log('i', f"Motion detected: { connection.cam_id }")
                connection.motion_detections.append((frame, label))

    print_log('i', f"Finishing motion detection on camera: { connection.cam_id }")

# class MotionDetector(Thread):    
#     def __init__(self, connection):
#         Thread.__init__(self)
#         self.__connection__ = connection        
#         self.__ready_motion_detection__ = True
#         self.__frame__ = None
#     def run(self):
#         """ Method to detect motion from static frames """
#         static_back = None
#         motion_list = [None, None] # List when any moving objct appear
#         time = [] # Time of movement
#         while self.__ready_motion_detection__:
#             self.__frame__ = self.__connection__.get_frame() #reading frame(image) from video 
#             motion = 0 #no motion
#             gray = cv2.cvtColor(self.__frame__, cv2.COLOR_BGR2GRAY) #converting color image to gray_scale image
#             # Converting gray scale image to GaussianBlur so that change can be find easily
#             gray = cv2.GaussianBlur(gray, (21, 21), 0)
#             # In first iteration we assing the value of static_back to our first frame
#             if static_back is None:
#                 static_back = gray
#                 continue
#             # Difference between static background and current frame(wich is GaussianBlur)
#             diff_frame = cv2.absdiff(static_back, gray)
#             # If change in between static background and current frame is grather than 30 it will show white color(255)
#             thresh_frame = cv2.threshold(diff_frame, 30, 255, cv2.THRESH_BINARY)[1]
#             thresh_frame = cv2.dilate(thresh_frame, None, iterations=5)
#             # Finding contour of moving object
#             cnts, _ = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#             for contour in cnts:
#                 area = cv2.contourArea(contour)
#                 if area > 100000 or area < 200 : continue
#                 motion = 1
#                 (x, y, w, h) = cv2.boundingRect(contour)
#                 # making green rectangle arround the moving object
#                 cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 1)
#             motion_list.append(motion) # Appending status of motion
#             motion_list = motion_list[-2:]
#             # Appending Start time of motion
#             if motion_list[-1]==1 and motion_list[-2]==0:
#                 time.append(datetime.now())