from detectors.fire_detector import FireDetector
from detectors.motion_detector import MotionDetector
from detectors.people_detector import PeopleDetector

from live_streaming import LiveStreaming
from settings import get_stream_folder_name, get_media_folder_name, get_captures_folder_name, get_index_stream_file_name

from util.directory import make_dir, delete_dir, is_dir, join_path, get_root_path
from util.logger import print_log
from util.date import get_current_time_string, get_current_raw_time
from frames_receiver import FramesReceiver
from threading import Thread

from db_manager import select_cameras_by_id_camera, insert_camera, insert_log

import cv2
import time
import os.path

class Connection(Thread):
    
    def __init__(self, id_uuid4, connector, address, db_conn, tcp_server):
        """ Method to create a connection from  """
        Thread.__init__(self)
        self.__uuid__ = id_uuid4
        self.__connector__ = connector
        self.__addr__ = address
        self.__running__ = True
        self.__db_connection__ = db_conn 
        self.__tcp_server__ = tcp_server
        self.__frame__ = None
    
    def run(self):
        """ Method to read frames from camera """
        
        # self.init_detectors()
        camera_id_from_cam = self.__connector__.recv(1024)  # receive cam_id from camera
        self.__cam_id__ = camera_id_from_cam.decode()

        if not self.__tcp_server__.is_camera_connected(self.__cam_id__):
            self.__tcp_server__.reg_connections(self.__cam_id__)
            print_log('i', f'New Connection : {self.__addr__}')
            print_log('i', f'Camera : {self.__cam_id__} connected')
            self.__tcp_server__.print_number_of_connections()
            
            self.path_this_camera = self.create_folder_dir() # create folder 
            cap_folder_name = join_path(self.path_this_camera, get_captures_folder_name())
            str_folder_name = join_path(self.path_this_camera, get_stream_folder_name())
            to_stream = join_path(str_folder_name, get_index_stream_file_name())

            id_camera_db = self.log_new_camera(self.path_this_camera) #database
            self.log_camera_connected(id_camera_db)  # log camera connected

            self.frame_receiver = FramesReceiver(self.__connector__)
            self.frame_receiver.start()

            self.live_streaming = LiveStreaming(self, to_stream, 'hls', 10)
            self.live_streaming.start()
            
            while self.__running__:
                try:
                    time.sleep(0.1)
                    frame = self.frame_receiver.get_frame()    
                    if frame is not None:
                        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        self.__frame__ = frame
                        self.__frame_to_fire_detector__ = frame
                        self.__frame_to_human_detector__ = frame
                        file_name = f'{join_path(cap_folder_name, self.get_pic_label())}'
                        cv2.imwrite(file_name, frame)
                    else:
                        self.stop_connection()
                except KeyboardInterrupt:
                    self.stop_connection()
                    print_log('i', "Connection Closed")

            self.log_camera_connected(id_camera_db)  # log camera disconnected
        else:
            self.__connector__.send(b'ID Camera repeated.') #when connection is refused because there is id camera 
            self.__running__ = False

        self.__connector__.close() #close connection        
        self.live_streaming.stop_stream()

    def log_camera_connected(self, id_camera_db):
        """ Method to log camera conection """
        insert_log(
            self.__db_connection__, 
            (get_current_raw_time(), ('CONNECTED' if self.__running__ else 'DISCONNECTED'), id_camera_db)
        )

    def get_pic_label(self):
        """ Create a unique picture file name by time. """
        return f"capture-{self.__cam_id__}-{get_current_time_string()}.jpg"

    def log_new_camera(self, path):
        """ Method to log a new camera in cameras table database. """
        id_camera_db=0
        regs = select_cameras_by_id_camera(self.__db_connection__, self.__cam_id__)
        if len(regs)==0:
            id_camera_db = insert_camera(
                self.__db_connection__, (self.__cam_id__, get_current_raw_time(), path))
        else:
            id_camera_db = regs[0][0]
        return id_camera_db
    
    def create_folder_dir(self) -> str:
        """ Method to define a path to save pics and stream files. """
        media_path = join_path(get_root_path(), get_media_folder_name())
        if not is_dir(media_path):
            make_dir(media_path)
        current_cam_media_path = join_path(media_path, self.__cam_id__)
        if not is_dir(current_cam_media_path):
            make_dir(current_cam_media_path)
            make_dir(join_path(current_cam_media_path,
                    get_stream_folder_name()))  # stream folder
            make_dir(join_path(current_cam_media_path, 
                    get_captures_folder_name()))  # captures folder
        return current_cam_media_path
        
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
        delete_dir(self.path_this_camera)
    
    def get_camera_id(self):
        return self.__cam_id__