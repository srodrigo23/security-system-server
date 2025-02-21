"""
Author  : Sergio Rodrigo Cardenas Rivera
Email   : rodrigosergio93@gmail.com
Version : 1.0
GitHub  : @srodrigo23
"""

import socket as skt
import uuid
import random
import settings as s
from util.logger import print_log
from connection import Connection

HOST = s.get_host()
PORT = random.randint(49152, 65535)

NUMBER_CONNECTIONS = 10
class TCPServer:
    """
    Code to run a server to manage socket connections
    """

    def __init__(self, server_mode:str) -> None:
        """
        Method to init a TCPServer class from host and port.
        """
        self.socket             = None
        self.tcp_server_running = True
        self.connections        = {}    # to store every Connection object
        self.id_cameras         = set() # id cameras
        self.define_server_mode(server_mode)

    def define_server_mode(self, actual_mode:str) -> None:
        """
        Method to turnOn detectors by command line argumnets
        """
        if actual_mode is not None:
            mode = actual_mode.lower()
            if mode =="f":
                s.set_fire_detector_status(enabled="true")

                s.set_motion_detector_status(enabled="false")
                s.set_people_detector_status(enabled="false")
                s.set_stream_enabled(enabled="false")

            elif mode == "m":
                s.set_motion_detector_status(enabled="true")

                s.set_fire_detector_status(enabled="false")
                s.set_people_detector_status(enabled="false")
                s.set_stream_enabled(enabled="false")

            elif mode == "p":
                s.set_people_detector_status(enabled="true")

                s.set_motion_detector_status(enabled="false")
                s.set_fire_detector_status(enabled="false")
                s.set_stream_enabled(enabled="false")            
            elif mode == "s":
                s.set_stream_enabled(enabled="true")

                s.set_people_detector_status(enabled="false")
                s.set_motion_detector_status(enabled="false")
                s.set_fire_detector_status(enabled="false")
        self.status_stream = s.get_stream_enabled()
        self.status_fire_detector = s.get_fire_detector_status()
        self.status_motion_detector = s.get_motion_detector_status()
        self.status_people_detector = s.get_people_detector_status()
        self.whatsapp_phone_number = s.get_phone_number_client()

    def prepare_server(self) -> None:
        """
        Method to prepare TCPServer from host and port to store connection object referencies.
        """
        print_log('i', "****** Welcome to the TCP-Server ******")
        try:
            self.socket = skt.socket(skt.AF_INET, skt.SOCK_STREAM)
            self.socket.bind((HOST, PORT))
            self.socket.listen(NUMBER_CONNECTIONS)
            self.show_initial_status()
        except skt.error as error:
            print(str(error))

    def show_initial_status(self) -> None:
        """
        Show on console initial server status
        """
        print_log('i', f"Serving on : {HOST} on port : {PORT}")
        print_log('i', f"Fire detector enabled    : {self.status_fire_detector}")
        print_log('i', f"People detector enabled  : {self.status_people_detector}")
        print_log('i', f"Motion detector enabled  : {self.status_motion_detector}")
        print_log('i', f"Streaming enabled        : {self.status_stream}")
        print_log('i', f"Whatsapp number to notif : {self.whatsapp_phone_number}")

    def run(self) -> None:
        """
        Method to keep alive waiting to more connections.
        """
        print_log('i', "Listen connections : ")
        while self.tcp_server_running:
            try:
                connector, address = self.socket.accept()
                ident = uuid.uuid4()
                self.connections[ident] = Connection(
                    id_uuid4=ident,
                    connector=connector,
                    address=address,
                    tcp_server=self
                )
                self.connections[ident].start()
            except skt.error as _e_:
                print('socket error', _e_)
            except KeyboardInterrupt:
                self.tcp_server_running = False
                self.stop_all_connections()
                self.close_detectors()
                print_log('i', "Server turned-off from keyboard")

    def reg_connections(self, id_camera) -> None:
        """
        Log if a camera has not been connected prevoiusly.
        """
        self.id_cameras.add(id_camera)

    def close_detectors(self) -> None:
        """
        To reg turned off detectors from config file
        """
        s.set_fire_detector_status(enabled="false")
        s.set_motion_detector_status(enabled="false")
        s.set_people_detector_status(enabled="false")
        s.set_stream_enabled(enabled="false")

    def is_connected(self, id_camera):
        """
        Check if id_camera is already in actual connections.
        """
        return id_camera in self.id_cameras

    def stop_all_connections(self) -> bool:
        """
        Stop all connections that have been created.
        """
        for connection in self.connections.values():
            if connection.running:
                connection.stop_detectors()
                connection.stop_connection()
                connection.join()
        print_log('i', "Stop all running connections")
        
    def print_number_of_connections(self) -> None:
        """
        Method to print logging number of connections.
        """
        # cont=0
        # for connection in self.connections.values():
        #     # if connection.running:
        #     cont = cont + 1
        print_log('i', f'Number of Connections : {len(self.connections)}')

    def delete_id_camera(self, id_camera:str, uuid_camera:str):
        """
        Method to delete id camera connection.
        """
        if id_camera in self.id_cameras:
            self.connections.pop(uuid_camera, None)
            self.id_cameras.remove(id_camera)

    def get_connections_info(self, actual_cam_id:str) -> list:
        """
        Method to get get connections info
        """
        cams_info = []
        if len(self.connections):
            for key in self.connections:
                actual_thread = self.connections[key]
                if actual_thread.get_camera_id() != actual_cam_id and\
                    actual_thread.running:
                    cams_info.append({
                        'id': actual_thread.get_camera_id(),
                        'time_connection' : actual_thread.time_info[0],
                        'date_connection': actual_thread.time_info[1],
                        'link': actual_thread.stream_link,
                    })
        return cams_info
