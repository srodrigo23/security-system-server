import cv2, sys
import time

cap = cv2.VideoCapture('tiktok.mp4')                    # 0 is for /dev/video0
while True :
    ret, frm = cap.read()
    # print(type(frm))
    # _, frm = cv2.imencode('.JPEG', frm)
    # frm = frm.tostring()
    time.sleep(1)
    sys.stdout.write(frm.tobytes())
    