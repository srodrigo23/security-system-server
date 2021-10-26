# import required libraries
from vidgear.gears import CamGear
from vidgear.gears import StreamGear
import cv2
import time

# open any valid video stream(for e.g `foo1.mp4` file)
stream = CamGear(source='../video/tiktok2.mp4').start()

# enable livestreaming and retrieve framerate from CamGear Stream and
# pass it as `-input_framerate` parameter for controlled framerate
stream_params = {"-input_framerate": 
    # stream.framerate, 
    30,
    "-livestream": True}

# describe a suitable manifest-file location/name
streamer = StreamGear(output="../live2/hls_out.m3u8", format = 'hls', **stream_params)

# loop over
while True:

    # read frames from stream
    frame = stream.read()

    # check for frame if Nonetype
    if frame is None:
        break

    # {do something with the frame here}
    # time.sleep(0.5)
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
