from detectors import fire_detector, people_detector, motion_detector
from live_streaming import LiveStreaming
from util.directory import make_dir, delete_dir, is_dir, join_path, get_root_path
from util.logger import print_log
from util.date import get_current_time_string, get_current_raw_time, get_date, get_time
from frames_receiver import FramesReceiver
from db_manager import select_cameras_by_id_camera, insert_camera, insert_log
from _thread import start_new_thread
from mail import mail_controller
from threading import Thread

import cv2
import time
import os.path
import copy
import settings as s

def log_camera_connected(db_connection, id_camera, running, time):
    """
    Method to log camera conection in database
    """
    insert_log(db_connection, 
        (time, ('CONNECTED' if running else 'DISCONNECTED'), id_camera)
    )

def create_folder_dir(cam_id):
    """ 
    Method to define a path to save pics and stream files.
    """
    media_path = join_path(get_root_path(), s.get_media_folder_name())
    if not is_dir(media_path):
        make_dir(media_path)
    current_cam_media_path = join_path(media_path, cam_id)
    if not is_dir(current_cam_media_path):
        make_dir(current_cam_media_path)
        make_dir(join_path(current_cam_media_path, s.get_stream_folder_name()))    # stream folder
        make_dir(join_path(current_cam_media_path, s.get_captures_folder_name()))  # captures folder
    return current_cam_media_path

def get_file_name(cap_folder_name, cam_id) -> str:
    """
    Create a unique picture file name by time.
    """
    return join_path(cap_folder_name, f"capture-{cam_id}-{get_current_time_string()}.jpg")

def log_new_camera(db_connection, cam_id, path) -> str:
    """
    Method to log a new camera in cameras table database.
    """
    id_camera_db = 0
    regs = select_cameras_by_id_camera(db_connection, cam_id)
    if len(regs)==0:
        id_camera_db = insert_camera(db_connection, (cam_id, get_current_raw_time(), path))
        print(f'this is the Id_camera_db {id_camera_db}')
    else:
        id_camera_db = regs[0][0]
    # print(f'this is the Id_camera_db {id_camera_db}')
    return id_camera_db

status_fire_detector = s.get_fire_detector_status()
status_motion_detector = s.get_motion_detector_status()
status_people_detector = s.get_people_detector_status()

class Connection(Thread):
    
    def __init__(self, id_uuid4, connector, address, db_conn, tcp_server):
        Thread.__init__(self)
        self.uuid = id_uuid4
        self.connector = connector
        self.addr = address
        self.running = True
        self.db_connection = db_conn 
        self.tcp_server = tcp_server
        
        self.stream_enabled = s.get_stream_enabled()
        self.stream_link = None
        
        
        self.define_storage_frames()
        self.define_storage_detections()
        self.amount_detections = 5
    
    def run(self):
        self.cam_id = self.connector.recv(4096).decode()

        if not self.tcp_server.is_connected(self.cam_id):
            self.tcp_server.reg_connections(self.cam_id)

            print_log('i', f'New Connection : { self.addr }')
            print_log('i', f'Camera : { self.cam_id } connected')

            self.tcp_server.print_number_of_connections()
            
            self.frame_receiver = FramesReceiver(self.connector)
            self.frame_receiver.start()
            
            path_this_camera = create_folder_dir(self.cam_id)
            
            if self.stream_enabled:     
                cap_folder_name = join_path(path_this_camera, s.get_captures_folder_name())
                str_folder_name = join_path(path_this_camera, s.get_stream_folder_name())
                to_stream = join_path(str_folder_name, s.get_index_stream_file_name())
                
                self.live_streaming = LiveStreaming(self, to_stream, 'hls', 10)
                self.live_streaming.start()
                self.stream_link = f'localhost:5000/{self.cam_id}/stream/index.h3m8'
            
            id_camera_db = log_new_camera(
                self.db_connection, 
                self.cam_id, 
                path_this_camera)
            log_camera_connected(
                self.db_connection, 
                id_camera_db, 
                self.running,
                time=get_current_raw_time())  # log camera connected
            
            self.init_process_sending_mail()
            
            if status_fire_detector:
                start_new_thread(fire_detector.detector, (self,))
            if status_motion_detector:
                start_new_thread(motion_detector.detector, (self,))
            if status_people_detector:
                start_new_thread(people_detector.detector, (self,))
                
            vb = True
            while self.running:
                try:
                    if vb:
                        time.sleep(0.25)
                        vb = False
                    time.sleep(0.1)
                    frame = self.frame_receiver.get_frame()
                    if frame is not None:
                        self.store_frame(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), get_current_time_string)
                        #TODO to improve
                        if status_fire_detector or status_motion_detector or status_people_detector: 
                            cv2.imwrite(get_file_name(cap_folder_name, self.cam_id), frame)
                    else:
                        self.stop_connection()
                except KeyboardInterrupt:
                    self.stop_connection()
                    print_log('i', "Connection Closed")
            
            log_camera_connected(
                self.db_connection,
                id_camera_db,
                self.running,
                time=get_current_raw_time())  # log camera connected
            
            self.init_process_sending_mail()
        else:
            self.running = False
            self.connector.send(b'ID Camera repeated.') #when connection is refused because there is id camera 

        self.connector.close() #close connection        
        if self.stream_enabled : 
            self.live_streaming.stop_stream()
            delete_dir(path_this_camera)
    
    def init_process_sending_mail(self) -> None:
        """
        Start thread to send event mail.
        """
        thread = Thread(
            target=self.send_mail_notification_connection,
            args=(
                self.cam_id, 
                self.running, 
                f"{self.stream_link if self.stream_enabled else ''}"))
        thread.start()
        
    def send_mail_notification_connection(self, cam_id:str, running:bool, link_stream:str)-> None:
        """"
        Method to send mail when connect/disconnect a camera
        """
        mail_controller.send_mail_camera_event_connection(
            camera_info={
                'id': cam_id,
                'time_connection': get_time(),
                'date_connection': get_date()
            },
            status=running,
            link=f'http://{link_stream}' if (running and link_stream != '') else '',
        )
        print_log(
            'i', f"{'Mail sended : Connected Camera' if running else 'Mail Sended : Disconnected Camera'}")
        
    
    def stop_connection(self):
        """
        Method to stop connection
        """
        self.running = False
        print_log('i', "Connection Closed")
        if self.stream_enabled: self.live_streaming.stop_stream()
        self.tcp_server.delete_id_camera(self.cam_id)
        self.tcp_server.print_number_of_connections()
    
    def store_frame(self, frame, date_time):
        """
        Method to store frames in queue
        """
        if status_fire_detector:
            self.store_frame_in_queue(
                self.fire_detection_queue, frame, date_time)
        if status_motion_detector:
            self.store_frame_in_queue(
                self.motion_detection_queue, frame, date_time)
        if status_people_detector:
            self.store_frame_in_queue(
                self.people_detection_queue, frame, date_time)
        if self.stream_enabled:
            self.store_frame_in_queue(
                self.stream_queue, frame, date_time)

    def store_frame_in_queue(self, queue, frame, date_time):
        """
        Generic method to store frames
        """
        if queue.full():  queue.get()
        else: queue.put((copy.deepcopy(frame), date_time))

    def define_storage_frames(self):
        """
        Method to define queues to store frames
        """
        from queue import Queue
        
        if status_fire_detector:
            self.fire_detection_queue = Queue(maxsize=200)
        if status_people_detector:
            self.people_detection_queue = Queue(maxsize = 200)
        if status_motion_detector:
            self.motion_detection_queue = Queue(maxsize = 200)
        if self.stream_enabled:
            self.stream_queue = Queue(maxsize = 200)
    
    def define_storage_detections(self):
        """
        Method to define detections store
        """
        if status_fire_detector:
            self.fire_detections = []
        if status_people_detector:
            self.people_detections = []
        if status_motion_detector:
            self.motion_detections = []

    def save_caption(self, path,frame, label):
        pass

    def save_and_mail(self, folder_name):
        pass

    def put_fire_detection(self, frame):
        len_list = len(self.fire_detections)
        if len_list > 20:
            to_save = self.fire_detections[0::int(len_list / 5)]
            # self.fire_detections[]
            self.save_and_mail('fire')
    

    def put_people_detection(self, frame):
        len_list = len(self.people_detections)
        if len_list > 20:
            to_save = self.fire_detections[0::int(len_list / 5)]
            self.save_and_mail('people')
    
    def put_motion_detection(self, frame):
        len_list = len(self.motion_detections)
        if len_list > 20:
            to_save = self.fire_detections[0::int(len_list / 5)]
            self.save_and_mail('motion')
        
    def get_frame(self, objetive='stream'):
        """
        To return the frame recieved from node to be readed by a client.
        """
        if objetive == 'fire_detector':
            return self.fire_detection_queue.get()
        elif objetive == 'motion_detector':
            return self.motion_detection_queue.get()
        elif objetive == 'people_detector':
            return self.people_detection_queue.get()
        else:
            return self.stream_queue.get()
        
    def get_camera_id(self):
        """
        Method to return camera id to show in the live streaming view
        """
        return self.cam_id