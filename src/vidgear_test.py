# https: // newbedev.com/pipe-raw-opencv-images-to-ffmpeg
from vidgear.gears import WriteGear
import cv2

# define (Codec,CRF,preset) FFmpeg tweak parameters for writer
output_params = {"-vcodec": "libx264", "-crf": 0, "-preset": "fast"}

# Open live webcam video stream on first index(i.e. 0) device
stream = cv2.VideoCapture('../media/tiktok.mp4')

writer = WriteGear(output_filename='Output.mp4', 
                   compression_mode=True, logging=True, 
                   **output_params)  # Define writer with output filename 'Output.mp4'

while True:  # infinite loop
    (grabbed, frame) = stream.read() # read frames
    if not grabbed:  # check if frame empty
        break  # if True break the infinite loop

    # {do something with frame here}
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    writer.write(gray)  # write a modified frame to writer
    cv2.imshow("Output Frame", frame)  # Show output window
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):  # check for 'q' key-press
        break  # if 'q' key-pressed break out

cv2.destroyAllWindows() # close output window
stream.release() # safely close video stream
writer.close() # safely close writer
