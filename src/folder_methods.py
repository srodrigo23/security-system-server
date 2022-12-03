"""
Methods to work with directories
"""
from util.directory import make_dir
from util.directory import is_dir
from util.directory import join_path
from util.directory import get_root_path
from util.directory import go_up

def create_media_dir_tree_to_new_connection(
    cam_id:str,
    media_folder_name:str,
    stream_folder_name:str,
    captures_folder_name:str) -> (str, str, str):
    """
    Method to define a path to save pics and stream files.
    """
    fire_detections_folder_name     = "fire_detections"
    movement_detections_folder_name = "movement_detections"
    human_detections_folder_name    = "human_detections"
    # go_up()
    root_path = get_root_path()
    media_path = join_path(
        root_path,
        media_folder_name
    )
    if not is_dir(media_path):
        make_dir(media_path)
    cam_media_path = join_path(
        media_path,
        cam_id
    )
    cam_media_pictures_path = join_path(
        cam_media_path,
        captures_folder_name
    )
    cam_media_stream_path = join_path(
        cam_media_path,
        stream_folder_name
    )
    cam_media_captures_fire_detections_path = join_path(
        cam_media_pictures_path,
        fire_detections_folder_name
    )
    cam_media_captures_movement_detections_path = join_path(
        cam_media_pictures_path,
        movement_detections_folder_name
    )
    cam_media_captures_human_detections_path = join_path(
        cam_media_pictures_path,
        human_detections_folder_name
    )
    if not is_dir(cam_media_path):
        make_dir(cam_media_path)
        make_dir(cam_media_pictures_path)
        make_dir(cam_media_stream_path)
        make_dir(cam_media_captures_fire_detections_path)
        make_dir(cam_media_captures_movement_detections_path)
        make_dir(cam_media_captures_human_detections_path)
    return (
        cam_media_stream_path,
        cam_media_captures_fire_detections_path,
        cam_media_captures_movement_detections_path,
        cam_media_captures_human_detections_path,
        cam_media_path
    )