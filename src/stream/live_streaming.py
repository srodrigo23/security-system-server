# import required libraries
from vidgear.gears import CamGear
from vidgear.gears import StreamGear
import cv2
import time

# output : "../live2/hls_out.m3u8"
# format : 'hls'

#vidgear

def live_streamming(output -> str, format -> str):
    stream = CamGear(source='0').start()
    stream_params = {"-input_framerate": stream.framerate, "-livestream": True}
    streamer = StreamGear(output=output, format = format, **stream_params)
    while True:
        frame = stream.read()
        if frame is None: 
            break
        # {do something with the frame here}
        streamer.stream(frame)  # send frame to streamer
        cv2.imshow("Output Frame", frame) 
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
    cv2.destroyAllWindows()
    stream.stop() 
    streamer.terminate()
    
live_streamming(output = "../live2/hls_out.m3u8", format = 'hls')
