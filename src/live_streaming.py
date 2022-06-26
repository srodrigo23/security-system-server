from vidgear.gears import StreamGear
from threading import Thread
from util.logger import print_log
from util.date import get_date, get_time

import cv2
import time

class LiveStreaming(Thread):
    """
    output : "../live2/hls_out.m3u8"
    format : 'hls'
    live_streamming(output = "../live2/hls_out.m3u8", format = 'hls')
    """

    def __init__(self, source, output_path, output_format, frame_rate):
        """ Method to init thread to stream video from a camera """
        Thread.__init__(self)
        self.__source__ = source # origin to get frames to stream
        stream_params = {
                "-input_framerate": frame_rate, 
                "-livestream": True
            }
        
        self.__streamer__ = StreamGear(output=output_path, format = output_format, **stream_params)
        self.__stream__ = True
        
    def run(self):
        """ Method that make stream from frames stored on every connection """
        while self.__stream__:
            frame = self.__source__.get_frame()
            if frame is not None:
                time.sleep(0.1)
                frame = self.put_text(self.__source__.get_camera_id(), frame, get_date(), get_time())
                try:
                    self.__streamer__.stream(frame)
                except Exception as e: 
                    print_log('w', f"Interrupted transmission: {e}")

        print_log('i', "Stream terminated")
        self.__streamer__.terminate()
    
    def stop_stream(self):
        """ Method to stop streamming """
        self.__stream__ = False
    
    def put_text(self, id, frame, date, time):
        font = cv2.FONT_HERSHEY_SIMPLEX
        
        font_scale = 1
        color = (255, 0, 0)
        thickness = 2
        org = (20, 40)
        text = f"CAMERA : {id}"
        frame = cv2.putText(frame, text, org, font, font_scale, color, thickness, cv2.LINE_AA)
        org = (20, 70)
        text = f"DATE : {date}"
        frame = cv2.putText(frame, text, org, font, font_scale, color, thickness, cv2.LINE_AA)
        org = (20, 100)
        text = f"TIME : {time}"
        frame = cv2.putText(frame, text, org, font, font_scale, color, thickness, cv2.LINE_AA)
        return frame