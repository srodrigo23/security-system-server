from threading import Thread

import numpy as np
import cv2
import time

class PeopleDetector(Thread):
    """
    PEOPLE DETECTION USING HOG
    https://thedatafrog.com/en/articles/human-detection-video/
    """
    def __init__(self, connection, fb_admin):
        """
        Method to initialize People detector
        """
        # initialize the HOG descriptor/person detector
        Thread.__init__(self)
        self.__hog__ = cv2.HOGDescriptor()
        self.__hog__.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        self.__connection__ = connection
        self.__fb_admin__ = fb_admin
        self.__frame__ = None
            
    def run(self):
        """
        Method to run people detection
        """
        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()
            time.sleep(0.1)
            # resizing for faster detection
            frame = cv2.resize(frame, (640, 480))
            # using a greyscale picture, also for faster detection
            gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            # detect people in the image
            # returns the bounding boxes for the detected objects
            boxes, weights = hog.detectMultiScale(frame, winStride=(8,8) )
            boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])
            for (xA, yA, xB, yB) in boxes:
                # display the detected boxes in the colour picture
                cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)
            # Write the output video 
            # out.write(frame.astype('uint8'))
            # Display the resulting frame
            # cv2.imshow('frame', frame)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break
        # When everything done, release the capture
        cap.release()
        # and release the output
        out.release()
        # finally, close the window
        cv2.destroyAllWindows()
        cv2.waitKey(1)