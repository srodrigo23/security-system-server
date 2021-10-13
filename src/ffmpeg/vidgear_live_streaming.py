# import required libraries
from vidgear.gears import CamGear
from vidgear.gears import StreamGear
import cv2

# open any valid video stream(for e.g `foo1.mp4` file)
stream = CamGear(source=0).start()

# describe a suitable manifest-file location/name
streamer = StreamGear(output="dash_out.mpd")

# loop over
while True:

    # read frames from stream
    frame = stream.read()

    # check for frame if Nonetype
    if frame is None:
        break

    # {do something with the frame here}

    # send frame to streamer
    streamer.stream(frame)

    # Show output window
    cv2.imshow("Output Frame", frame)

    # check for 'q' key if pressed
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

# close output window
cv2.destroyAllWindows()

# safely close video stream
stream.stop()

# safely close streamer
streamer.terminate()