import cv2
# from threading import Thread
# from util.logger import print_log
print('fire detector imported')

fire_cascade = cv2.CascadeClassifier('classifiers/fire_detection.xml')

def detector(frame, list):
    print('trying to detect fire')
    fire_cascade = cv2.CascadeClassifier('fire_detection.xml')
    fire = fire_cascade.detectMultiScale(frame, 1.2, 5)
    for (x,y,w,h) in fire:
        cv2.rectangle(frame, (x-20, y-20), (x+w+20, y+h+20), (255,0,0), 2)
    if len(fire) > 0:
        list.add(frame)
        # return True, frame

    # return False, None


# class FireDetector(Thread):
#     def __init__(self, connection):
#         Thread.__init__(self)

#         self.fire_cascade = cv2.CascadeClassifier('fire_detection.xml')
#         self.connection = connection
#         self.running = True
#         self.captures = []
        
#     def run(self):
#         """
#         Method to execute detector.
#         """
#         while self.running:
#             time.sleep(0.1) # to prevent overcharge cpu
#             frame = self.connection.get_frame()
#             # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#             fire = self.fire_cascade.detectMultiScale(frame, 1.2, 5)
                        
#             for (x,y,w,h) in fire:
#                 cv2.rectangle(frame, (x-20, y-20), (x+w+20, y+h+20), (255,0,0), 2)
#                 if len(self.captures) < 10
#                     self.captures.add(frame)

#                 # roi_gray = gray[y:y+h, x:x+w]
#                 # roi_color = frame[y:y+h, x:x+w]
                