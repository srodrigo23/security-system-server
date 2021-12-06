# import required libraries
from vidgear.gears import CamGear
from vidgear.gears import StreamGear
from threading import Thread
from settings import get_path_folder_streaming
from util.directory import make_dir
from util.directory import delete_dir

import cv2
import time

class LiveStreaming(Thread):
    """
    output : "../live2/hls_out.m3u8"
    format : 'hls'
    live_streamming(output = "../live2/hls_out.m3u8", format = 'hls')
    """
    
    def __init__(self, source, output_path, output_format, frame_rate):
        """
        Method to init thread to stream video from a camera
        """
        Thread.__init__(self)
        self.__source__ = source # origin to get frames to stream
        stream_params = {
            "-input_framerate": frame_rate, 
            "-livestream": True
            }
        
        
        self.__streamer__ = StreamGear(output=output_path, format = output_format, **stream_params)
        self.__stream__ = True
        
    
    def run(self):
        """
        Method that make stream from frames stored on every connection
        """
        while self.__stream__:
            frame = self.__streamer__.read()
            if frame is None:
                self.__stream__ = False
            else:
                self.__streamer__.stream(frame)
        self.__streamer__.terminate()