"""
Method to people detection
"""
import time
import numpy as np
import cv2
from util.logger import print_log

def detector(connection):
    """
    Method to people detection
    """
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(
        cv2.HOGDescriptor_getDefaultPeopleDetector()
    )
    print_log('i', f"People detection on camera: { connection.cam_id }")
    time.sleep(2)
    while connection.running:
        time.sleep(0.1)
        frame, label = connection.get_frame(objetive='people_detector')
        if frame is not None:
            gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            boxes, weights = hog.detectMultiScale(gray, winStride=(16,16) )
            # print(weights)
            boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])
            if len(boxes) > 0:
                print_log('i', f"People detected: { connection.cam_id }")
                connection.people_detections.append((frame, label))
                for (x, y, w, h) in boxes:
                    cv2.rectangle(frame, (x, y), (w, h), (0, 255, 0), 2)
    print_log('i', f"Finishing people detection on camera: { connection.cam_id }")

# class PeopleDetector(Thread):
#     def __init__(self, connection):
#         # initialize the HOG descriptor/person detector
#         Thread.__init__(self)
#         self.__hog__ = cv2.HOGDescriptor()
#         self.__hog__.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
#         self.__connection__ = connection
#         self.__frame__ = None
            
#     def run(self):
#         """ Method to run people detection """
#         while True:
#             # Capture frame-by-frame
#             ret, frame = cap.read()
#             time.sleep(0.1)
#             # resizing for faster detection
#             frame = cv2.resize(frame, (640, 480))
#             # using a greyscale picture, also for faster detection
#             gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
#             # detect people in the image
#             # returns the bounding boxes for the detected objects
#             boxes, weights = hog.detectMultiScale(frame, winStride=(8,8) )
#             boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])
#             for (xA, yA, xB, yB) in boxes:
#                 # display the detected boxes in the colour picture
#                 cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)
#             # Write the output video 
#             # out.write(frame.astype('uint8'))
#             # Display the resulting frame
#             # cv2.imshow('frame', frame)
#             # if cv2.waitKey(1) & 0xFF == ord('q'):
#             #     break
#         # When everything done, release the capture
#         cap.release()
#         # and release the output
#         out.release()
#         # finally, close the window
#         cv2.destroyAllWindows()
#         cv2.waitKey(1)