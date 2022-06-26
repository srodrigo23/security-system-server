from detectors import fire_detector
from detectors import people_detector
from detectors import motion_detector

from live_streaming import LiveStreaming

from settings import get_stream_folder_name, get_media_folder_name
from settings import get_captures_folder_name
from settings import get_index_stream_file_name

from util.directory import make_dir, delete_dir, is_dir, join_path, get_root_path
from util.logger import print_log
from util.date import get_current_time_string, get_current_raw_time

from frames_receiver import FramesReceiver
from threading import Thread
from db_manager import select_cameras_by_id_camera, insert_camera, insert_log
from _thread import start_new_thread

import cv2
import time
import os.path

def log_camera_connected(db_connection, id_camera, running):
    """
    Method to log camera conection in database
    """
    insert_log(db_connection, 
        (get_current_raw_time(), ('CONNECTED' if running else 'DISCONNECTED'), id_camera)
    )

def create_folder_dir(cam_id):
    """ 
    Method to define a path to save pics and stream files.
    """
    media_path = join_path(get_root_path(), get_media_folder_name())
    if not is_dir(media_path):
        make_dir(media_path)
    current_cam_media_path = join_path(media_path, cam_id)
    if not is_dir(current_cam_media_path):
        make_dir(current_cam_media_path)
        make_dir(join_path(current_cam_media_path, get_stream_folder_name()))    # stream folder
        make_dir(join_path(current_cam_media_path, get_captures_folder_name()))  # captures folder
    return current_cam_media_path

def get_file_name(cap_folder_name, cam_id):
    """
    Create a unique picture file name by time.
    """
    return join_path(cap_folder_name, f"capture-{cam_id}-{get_current_time_string()}.jpg")

def log_new_camera(db_connection, cam_id, path):
    """
    Method to log a new camera in cameras table database.
    """
    id_camera_db = 0
    regs = select_cameras_by_id_camera(db_connection, cam_id)
    if len(regs)==0:
        id_camera_db = insert_camera(db_connection, (cam_id, get_current_raw_time(), path))
    else:
        id_camera_db = regs[0][0]
    return id_camera_db

class Connection(Thread):
    
    def __init__(self, id_uuid4, connector, address, db_conn, tcp_server):
        Thread.__init__(self)
        self.uuid = id_uuid4
        self.connector = connector
        self.addr = address
        self.running = True
        self.db_connection = db_conn 
        self.tcp_server = tcp_server
        self.frame = None
        
        self.fire_detections = []
        self.people_detections = []
        self.motion_detections = []
    
    def run(self):
        self.cam_id = self.connector.recv(4096).decode()

        if not self.tcp_server.is_connected(self.cam_id):
            self.tcp_server.reg_connections(self.cam_id)

            print_log('i', f'New Connection : { self.addr }')
            print_log('i', f'Camera : { self.cam_id } connected')

            self.tcp_server.print_number_of_connections()
            
            path_this_camera = create_folder_dir(self.cam_id) # create folder 

            cap_folder_name = join_path(path_this_camera, get_captures_folder_name())
            str_folder_name = join_path(path_this_camera, get_stream_folder_name())

            to_stream = join_path(str_folder_name, get_index_stream_file_name())

            id_camera_db = log_new_camera(self.db_connection, self.cam_id, path_this_camera) #database
            log_camera_connected(self.db_connection, id_camera_db, self.running)  # log camera connected

            self.frame_receiver = FramesReceiver(self.connector)
            self.frame_receiver.start()

            # self.live_streaming = LiveStreaming(self, to_stream, 'hls', 10)
            # self.live_streaming.start()
            
            # start_new_thread(fire_detector.detector, (self,))
            # start_new_thread(people_detector.detector, (self,))
            start_new_thread(movement_detector.detector, (self,))

            while self.running:
                time.sleep(1)
                try:
                    frame = self.frame_receiver.get_frame()
                    if frame is not None:
                        self.frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        # print(len(self.fire_detections))
                        # print(len(self.people_detections))
                        print(len(self.motion_detections))
                        # cv2.imwrite(get_file_name(cap_folder_name, self.cam_id), frame)
                    else:
                        self.stop_connection()
                except KeyboardInterrupt:
                    self.stop_connection()
                    print_log('i', "Connection Closed")
            
            #para la desconeccion
            log_camera_connected(self.db_connection, id_camera_db, self.running)  # log camera disconnected
        else:
            self.connector.send(b'ID Camera repeated.') #when connection is refused because there is id camera 
            self.running = False
        print(f'end connection {self.running}')
        self.connector.close() #close connection        
        # self.live_streaming.stop_stream()
        delete_dir(path_this_camera)
    
    def get_frame(self):
        """
        To return the frame recieved from node to be readed by a client.
        """
        return self.frame
    
    def stop_connection(self):
        """
        Method to stop connection
        """
        self.running = False
        print_log('i', "Connection Closed")
        self.tcp_server.delete_id_camera(self.cam_id)
        self.tcp_server.print_number_of_connections()
        
    def get_camera_id(self):
        return self.cam_id