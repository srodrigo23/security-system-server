import cv2, sys
import time

# python test.py | ffmpeg -f rawvideo -pixel_format bgr24 -video_size 320x240 -framerate 15 -i - foo.avi
# python test.py | ffmpeg -y -f rawvideo -vcodec rawvideo -s 321x240 -pix_fmt rgba -framerate 15 -i - foo.mp4

stream = cv2.VideoCapture(0) # 0 is for /dev/video0
while True:
    (grabbed, frame) = stream.read()
    if not grabbed:
        break
    sys.stdout.write(str(frame.tostring()))
    cv2.imshow("Output Frame", frame)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

cv2.destroyAllWindows()
# close output window
stream.release()
# safely close video stream
