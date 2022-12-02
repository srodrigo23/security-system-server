"""
Method to stream video with StreamGear lib.
"""
from threading import Thread
import time
from vidgear.gears import StreamGear
import cv2
from util.logger import print_log
from util.date import get_date, get_time

class LiveStreaming(Thread):
    """
    output : "../live2/hls_out.m3u8"
    format : 'hls'
    live_streamming(output = "../live2/hls_out.m3u8", format = 'hls')
    """
    def __init__(self,
        source,
        output_path,
        output_format='hls',
        frame_rate=10) -> None:
        """
        Method to init thread to stream video from a camera
        """
        Thread.__init__(self)
        self.source = source # origin to get frames to stream
        # "-resolution": "640x360", "-framerate": "60.0"
        stream_params = {
            "-input_framerate": frame_rate, 
            "-livestream": True,
            "-streams":
                [
            #         # {"-resolution": "1920x1080", "-video_bitrate": "4000k"}, # Stream1: 1920x1080 at 4000kbs bitrate
            #         # {"-resolution": "1280x720", "-framerate": "30.0"}, # Stream2: 1280x720 at 30fps
                    {
                        "-resolution": "640x360", 
                        "-framerate": "30.0"
                    }  # Stream3: 640x360 at 60fps
                ]
        }
        self.streamer = StreamGear(
            output=output_path,
            format = output_format,
            **stream_params
        )
        self.stream = True
        
    def run(self):
        """
        Method that make stream from frames stored on every connection.
        """
        time.sleep(1)
        while self.__stream__:
            frame, date = self.source.get_frame()
            if frame is not None:
                time.sleep(0.1)
                frame = self.put_text(
                    self.source.get_camera_id(),
                    frame,
                    get_date(),
                    get_time())
                try:
                    self.streamer.stream(frame)
                except Exception as error:
                    print_log('w', f"Interrupted transmission: {error}")

        print_log('i', "Stream terminated")
        self.streamer.terminate()
    
    def stop_stream(self):
        """
        Method to stop streamming.
        """
        self.__stream__ = False
    
    def put_text(self, id, frame, text_date, text_time)->None:
        """
        Method to put text about cam id, time and date. 
        """
        font       = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        color      = (255, 0, 0)
        thickness  = 2
        frame = cv2.putText(
            frame, f"CAMERA : {id}", (20, 40), font,
            font_scale, color, thickness, cv2.LINE_AA
        )
        frame = cv2.putText(
            frame, f"DATE : {text_date}", (20, 70), font,
            font_scale, color, thickness, cv2.LINE_AA)
    
        frame = cv2.putText(
            frame, f"TIME : {text_time}", (20, 100), font,
            font_scale, color, thickness, cv2.LINE_AA)
        return frame