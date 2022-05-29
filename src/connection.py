from detectors.fire_detector import FireDetector
from detectors.motion_detector import MotionDetector
from detectors.people_detector import PeopleDetector

from live_streaming import LiveStreaming
from settings import get_path_folder_streaming

from util.directory import make_dir
from util.directory import delete_dir
from util.logger import print_log
from util.date import get_current_time_string
from frames_receiver import FramesReceiver
from threading import Thread

import cv2
import time

class Connection(Thread):
    
    def __init__(self, id_uuid4, connector, address, tcp_server):
        """ Method to create a connection from  """
        Thread.__init__(self)
        self.__uuid__ = id_uuid4
        self.__connector__ = connector
        self.__addr__ = address
        self.__running__ = True
        self.__tcp_server__ = tcp_server
        # self.__live_streaming__ = LiveStreaming(self, self.__path__, 'hls', 30)
    
    def run(self):
        """ Method to read frames from camera """
        # self.__live_streaming__.start()
        # self.init_detectors()
        self.__cam_id__ = self.__connector__.recv(1024)

        if not self.__tcp_server__.is_camera_connected(self.__cam_id__):
            self.__tcp_server__.reg_connections(self.__cam_id__)
            print_log('i', f"New Connection : {self.__addr__}")
            print_log('i', f'Camera : {self.__cam_id__.decode()} connected')
            self.__tcp_server__.print_number_of_connections()

            self.frame_receiver = FramesReceiver(self.__connector__)
            self.frame_receiver.start()
            
            while self.__running__: 
                time.sleep(0.2)
                frame = self.frame_receiver.get_frame()
                if frame is not None:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    self.__frame__ = frame
                    self.__frame_to_fire_detector__ = frame
                    self.__frame_to_human_detector__ = frame
                else:
                    self.stop_connection()
    
        self.__connector__.close() #close connection
        self.__running__ = False
        # delete_dir(self.__path__)
        # self.__live_streaming__.stop_stream()
        
    def init_detectors(self):
        """ Method to init and start detectors """
        self.__fire_detector__ = FireDetector(self, self.__fb_admin__)
        self.__fire_detector__.start()
        self.__people_detector__ = PeopleDetector(self, self.__fb_admin__)
        self.__people_detector__.start()
        self.__motion_detector__ = MotionDetector(self, self.__fb_admin__)
        self.__motion_detector__.start()

    def get_frame_to_fire_detector(self):
        """ Method to get frames to identify fire on frames """
        return self.__frame_to_fire_detector__

    def get_frame_to_human_detector(self):
        """ Method to get frames to identify fire on frames """
        return self.__frame_to_human_detector__
        
    def get_frame(self):
        """ To return the frame recieved from node to be readed by a client. """
        return self.__frame__
    
    def stop_connection(self):
        """ Method to stop connection """
        self.__running__ = False
        print_log('i', "Connection Closed")
        self.__tcp_server__.delete_id_camera(self.__cam_id__)
        self.__tcp_server__.print_number_of_connections()