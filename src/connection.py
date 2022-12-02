"""
Method ans classes to make connection
"""
from threading import Thread
from _thread import start_new_thread
from queue import Queue

import time
import copy
import cv2
import settings as s

from detectors import fire_detector
from detectors import people_detector
from detectors import motion_detector

from live_streaming import LiveStreaming
from frames_receiver import FramesReceiver
from mail import mail_controller

from util.logger import print_log
from util.date import get_current_time_string
from util.date import get_date
from util.date import get_time
from util.directory import delete_dir
from util.directory import join_path
from folder_methods import create_media_dir_tree_to_new_connection

status_fire_detector   = s.get_fire_detector_status()
status_motion_detector = s.get_motion_detector_status()
status_people_detector = s.get_people_detector_status()
stream_enabled         = s.get_stream_enabled()

class Connection(Thread):
    """
    Thread for each connection
    """
    def __init__(self, id_uuid4, connector, address, tcp_server):
        Thread.__init__(self)
        self.uuid       = id_uuid4
        self.connector  = connector
        self.addr       = address
        self.running    = True
        self.server     = tcp_server # reference
        self.stream_link = None
        self.cam_id     = None
        self.define_storage_frames()
        self.define_storage_detections()
        
    def start_stream(self, cam_id, path_folder_to_stream) -> None:
        """
        Method to stream video
        """
        live_streaming = None
        if stream_enabled:
            live_streaming = LiveStreaming(
                source=self,
                output_path=path_folder_to_stream,
                output_format='hls',
                frame_rate=1
            )
            live_streaming.start()
            self.stream_link = f"http://127.0.0.1:5000/{cam_id}/stream/index.m3u8"
        return live_streaming
    
    def start_detectors(self,
        path_fire_detections:str,
        path_motion_detections: str,
        path_people_detections: str) -> None:
        """
        Method to start detectors by config
        """
        if status_fire_detector :
            start_new_thread(
                fire_detector.detector,
                (self, path_fire_detections)
            )
        if status_motion_detector :
            start_new_thread(
                motion_detector.detector,
                (self, path_motion_detections)
            )
        if status_people_detector :
            start_new_thread(
                people_detector.detector,
                (self,path_people_detections)
            )
            
    def init_new_connection(self, cam_id:str) -> None:
        """
        Method to init and show info about new connection.
        """
        self.server.reg_connections(cam_id)
        print_log('i', f'New Connection : { self.addr }')
        print_log('i', f'Camera : {cam_id} connected')
        self.server.print_number_of_connections()
        
    def run(self) -> None:
        """
        Main execution
        """
        cam_id = self.connector.recv(4096).decode()
        self.cam_id = cam_id
        if not self.server.is_connected(cam_id):
            self.init_new_connection(
                cam_id=cam_id
            )
            frame_receiver = FramesReceiver(self.connector)
            frame_receiver.start()
            paths = create_media_dir_tree_to_new_connection(
                cam_id=cam_id,
                media_folder_name="media",
                stream_folder_name="stream",
                captures_folder_name="captures"
            )
            path_to_stream = join_path(
                paths[0],
                s.get_index_stream_file_name()
            )
            stream_thread = self.start_stream(
                cam_id=cam_id,
                path_folder_to_stream=path_to_stream
            )
            self.start_detectors(
                path_fire_detections=paths[1],
                path_motion_detections=paths[2],
                path_people_detections=paths[3],
            )
            self.send_notif_connection(  # connected
                cam_id=cam_id,
                running=self.running
            )
            self.loop_process(
                cam_id=cam_id,
                frame_receiver_thread=frame_receiver,
                stream_thread=stream_thread
            )
            self.send_notif_connection(  # disconnected
                cam_id=cam_id,
                running=self.running
            )
            delete_dir(paths[4])
        else:
            self.connector.send(b'ID Camera repeated.')
            # self.connector.close() #close connection
        # if self.stream_enabled:
        #     self.live_streaming.stop_stream()
        #     delete_dir(path_this_camera)

    def loop_process(self, cam_id, frame_receiver_thread, stream_thread) -> None:
        """
        Core method to receive frames and stream and detections
        """
        _vb_ = True
        while self.running:
            try:
                if _vb_:
                    time.sleep(0.25)
                    _vb_ = False
                time.sleep(0.1)
                frame = frame_receiver_thread.get_frame()
                if frame is not None:
                    self.store_frame(
                        cv2.cvtColor(frame, cv2.COLOR_BGR2RGB),
                        get_current_time_string()
                    )
                    if status_fire_detector    or\
                        status_motion_detector or\
                        status_people_detector:
                        pass
                        # cv2.imwrite(
                        #     get_file_name(
                        #         cap_folder_name,
                        #         self.cam_id
                        #     ),
                        #     frame
                        # )
                else:
                    self.stop_connection(cam_id, stream_thread)
            except KeyboardInterrupt:
                self.stop_connection(cam_id, stream_thread)
                print_log('i', "Connection Closed")
    
    def send_notif_connection(self, cam_id:str, running:bool)-> None:
        """
        Method to send mail when connect/disconnect a camera
        """
        mail_controller.send_mail_camera_event_connection(
            camera_info={
                'id': cam_id,
                'time_connection': get_time(),
                'date_connection': get_date()
            },
            status=running,
            link=self.stream_link,
            other_cams=[]
        )
        print_log(
            'i',
            f"{'Mail sended : Connected cam.'if running else'Mail Sended : Disconnected cam.'}"
        )

    def stop_connection(self, cam_id:str, stream_thread)->None:
        """
        Method to stop connection
        """
        self.running = False
        print_log('i', "Connection Closed")
        if stream_enabled:
            stream_thread.stop_stream()
        self.server.delete_id_camera(cam_id)
        self.server.print_number_of_connections()
    
    def store_frame(self, frame, date_time):
        """
        Method to store frames in queue
        """
        if status_fire_detector:
            self.store_frame_in_queue(
                self.fire_detection_queue,
                frame,
                date_time
            )
        if status_motion_detector:
            self.store_frame_in_queue(
                self.motion_detection_queue,
                frame,
                date_time
            )
        if status_people_detector:
            self.store_frame_in_queue(
                self.people_detection_queue,
                frame,
                date_time
            )
        if stream_enabled:
            self.store_frame_in_queue(
                self.stream_queue, frame, date_time)

    def store_frame_in_queue(self, queue, frame, date_time) -> None:
        """
        Generic method to store frames
        """
        if queue.full():
            queue.get()
        else:
            queue.put((copy.deepcopy(frame), date_time))

    def define_storage_frames(self) -> None:
        """
        Method to define queues to store frames
        """
        if status_fire_detector:
            self.fire_detection_queue = Queue(maxsize=200)
        if status_people_detector:
            self.people_detection_queue = Queue(maxsize = 200)
        if status_motion_detector:
            self.motion_detection_queue = Queue(maxsize = 200)
        if stream_enabled:
            self.stream_queue = Queue(maxsize = 200)
    
    def define_storage_detections(self) -> None:
        """
        Method to define detections store
        """
        if status_fire_detector:
            self.fire_detections = []
        if status_people_detector:
            self.people_detections = []
        if status_motion_detector:
            self.motion_detections = []

    # def send_event_notif(self, folder_captures_name:str, detection_name:str):
    #     pass

    # def put_fire_detection(self, frame):
    #     len_list = len(self.fire_detections)
    #     if len_list > 20:
    #         to_save = self.fire_detections[0::int(len_list / 5)]
    #         # self.fire_detections[]
    #         self.save_and_mail('fire')

    # def put_people_detection(self, frame):
    #     len_list = len(self.people_detections)
    #     if len_list > 20:
    #         to_save = self.fire_detections[0::int(len_list / 5)]
    #         self.save_and_mail('people')
    
    # def put_motion_detection(self, frame):
    #     len_list = len(self.motion_detections)
    #     if len_list > 20:
    #         to_save = self.fire_detections[0::int(len_list / 5)]
    #         self.save_and_mail('motion')
        
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