"""
Thread Class to define a new connection
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
from whatsapp import whatsapp_controller

from util.logger import print_log
from util.date import get_current_time_string
from util.date import get_date
from util.date import get_time
from util.directory import delete_dir
from util.directory import join_path
from util.directory import get_list_files
from folder_methods import create_media_dir_tree_to_new_connection
from folder_methods import make_file_detection_name
from storage.imagekit.store import upload_file

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
        self.server     = tcp_server #reference
        # self.time_info  = time_info
        # self.stream_link = None if stream_enabled is False else f"http://127.0.0.1:5000/{cam_id}/stream/index.m3u8"
        self.stream_link = None
        self.cam_id = None
        self.stream_thread = None
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
        # path_fire_detections:str,
        # path_motion_detections: str,
        # path_people_detections: str
        ) -> None:
        """
        Method to start detectors by config
        """
        if status_fire_detector :
            # start_new_thread(
            #     fire_detector.detector,
            #     (self,)
            # )
            thread = Thread(target=fire_detector.detector, args=(self,))
            thread.start()
            
        if status_motion_detector :
            start_new_thread(
                motion_detector.detector,
                (self,)
            )
        if status_people_detector :
            start_new_thread(
                people_detector.detector,
                (self,)
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
            self.stream_thread = self.start_stream(
                cam_id=cam_id,
                path_folder_to_stream=path_to_stream
            )
            self.start_detectors()
            self.send_notif_connection( #connected
                cam_id=cam_id,
                running=self.running
            )
            self.loop_process(
                frame_receiver_thread=frame_receiver,
                paths_to_detections=paths
            )
            self.send_notif_connection( #disconnected
                cam_id=cam_id,
                running=self.running
            )
            delete_dir(paths[4])
        else:
            self.connector.send(b'ID Camera repeated.')
            self.connector.close() #close connection
            self.running = False

    def loop_process(self,
        frame_receiver_thread,
        paths_to_detections:list) -> None:
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
                    self.make_notification(paths=paths_to_detections)
                else:
                    self.stop_connection()
            except KeyboardInterrupt:
                self.stop_connection()
                print_log('i', "Connection Closed")
        if stream_enabled:
            self.stream_thread.stop_stream()
    
    def send_notif_connection(self, cam_id:str, running:bool)-> None:
        """
        Method to send mail when connect/disconnect a camera
        """
        camera_info={
            'id': cam_id,
            'time_connection': get_time(),#self.time_info[0],
            'date_connection': get_date(),#self.time_info[1]
        }
        mail_controller.send_mail_camera_event_connection(
            camera_info=camera_info,
            status=running,
            link=self.stream_link,
            other_cams=self.server.get_connections_info(actual_cam_id=cam_id)
        )
        print_log(
            'i',
            f"{'Mail Sended : Connected camera'if running else'Mail Sended : Disconnected camera'}"
        )
        
        whatsapp_controller.send_message_event_camera_connection(
            camera_info=camera_info,
            status=running,
            link= True if self.stream_link is not None else False
        )
        print_log(
            'i',
            f"{'WhatsApp Message Sended : Connected camera'if running else'WhatsApp Message Sended : Disconnected camera'}"
        )

    def stop_connection(self)->None:
        """
        Method to stop connection
        """
        self.running = False
        print_log('i', "Connection Closed")
        if stream_enabled:
            self.stream_thread.stop_stream()
        self.server.delete_id_camera(self.cam_id)
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

    def send_event_notif(self,
        folder_captures_name:str,
        detection_name:str,
        event_info:dict)->None:
        """
        Send mail notification with captures,
        """
        attachments = get_list_files(folder_captures_name)
        print_log('i', f"Alert mail sended {detection_name}.")
        mail_controller.send_mail_camera_event_detection(
            detection_code=detection_name,
            detection_info=event_info, #dict about event
            attachments=attachments
        )

    def send_whatsapp_event_notif(self, url_list:list, event:str)->None:
        for url in url_list:
            whatsapp_controller.send_message_event_detection(
                type_detection=event,
                media_url=url
            )

    def make_fire_detection(self, path_to_detections:str) -> None:
        """
        Store fire detection
        """
        event='fire'
        len_detections = len(self.fire_detections)
        if len_detections >= 10:
            to_save = self.fire_detections[0::int(len_detections/5)]
            self.fire_detections = []
            url_detections = self.save_detections(
                detections=to_save,
                folder_path=path_to_detections
            )
            self.send_event_notif( #mail
                folder_captures_name=path_to_detections,
                detection_name=event,
                event_info={
                    'id': self.cam_id,
                    'time_detection': get_time(),
                    'date_detection': get_date(),
                    'link': self.stream_link
                }
            )
            self.send_whatsapp_event_notif(
                event="fire",
                url_list=url_detections
            )


    def make_people_detection(self, path_to_detections: str) -> None:
        """
        Store people  detection
        """
        event = 'people'
        len_detections = len(self.people_detections)
        if len_detections >= 10:
            to_save = self.people_detections[0::int(len_detections/5)]
            self.people_detections = []
            url_detections = self.save_detections(
                detections=to_save,
                folder_path=path_to_detections)
            self.send_event_notif(
                folder_captures_name=path_to_detections,
                detection_name=event,
                event_info={
                    'id': self.cam_id,
                    'time_detection': get_time(),
                    'date_detection': get_date(),
                    'link': self.stream_link
                }
            )
            self.send_whatsapp_event_notif(
                event="people",
                url_list=url_detections
            )
    
    def make_motion_detection(self, path_to_detections: str) -> None:
        """
        Store motion detection
        """
        event = 'motion'
        len_detections = len(self.motion_detections)
        if len_detections >= 10:
            to_save = self.motion_detections[0::int(len_detections/5)]
            self.motion_detections = []
            url_detections = self.save_detections(
                detections=to_save,
                folder_path=path_to_detections)
            self.send_event_notif(
                folder_captures_name=path_to_detections,
                detection_name=event,
                event_info={
                    'id': self.cam_id,
                    'time_detection': get_time(),
                    'date_detection': get_date(),
                    'link': self.stream_link
                }
            )
            # self.people_detections = []
            self.send_whatsapp_event_notif(
                event="people",
                url_list=url_detections
            )
        
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
        
    def get_camera_id(self)->str:
        """
        Method to return camera id to show in the live streaming view
        """
        return self.cam_id

    def make_notification(self, paths:list)->None:
        """
        Make a notification with some detections stored
        """
        if status_fire_detector:
            self.make_fire_detection(
                path_to_detections=paths[1]
            )
        if status_motion_detector:
            self.make_motion_detection(
                path_to_detections=paths[2]
            )
        if status_people_detector:
            self.make_people_detection(
                path_to_detections=paths[3]
            )

    def save_detections(self,
            detections:list, #frames and labels
            folder_path:str) -> list:
        """
        Make detection picture and save on directory
        """
        # import os
        url_detections=[]
        for capture, label in detections:
            file_name = make_file_detection_name(
                path=folder_path,
                file_name=label
            )
            cv2.imwrite(filename=file_name,img=capture)
            # path_to_file = os.path.join(folder_path, file_name)
            data_image_uploaded = upload_file(
                image_file=file_name, 
                file_label=label,
                
                path_to_upload=folder_path
            )
            url_detections.append(data_image_uploaded['url'])
        return url_detections