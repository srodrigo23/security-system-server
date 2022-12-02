"""
Methods to work with directories
"""
from util.directory import make_dir
from util.directory import delete_dir #to delete dirs
from util.directory import is_dir
from util.directory import join_path
from util.directory import get_root_path


def create_media_dir_tree_to_new_connection(
    cam_id:str,
    root_path:str,
    media_folder_name:str,
    stream_folder_name:str,
    captures_folder_name:str) -> (str, str, str):
    """
    Method to define a path to save pics and stream files.
    """
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
        stream_folder_name
    )
    cam_media_stream_path = join_path(
        cam_media_path,
        captures_folder_name
    )
    if not is_dir(cam_media_path):
        make_dir(cam_media_path) #create folder
        make_dir(cam_media_pictures_path)
        make_dir(cam_media_stream_path)
    return cam_media_path, cam_media_pictures_path, cam_media_stream_path


def create_folder()->None:
    cap_folder_name = join_path(
        camera_path,
        s.get_captures_folder_name()
    )
    str_folder_name = join_path(
        camera_path,
        s.get_stream_folder_name()
    )
    to_stream = join_path(
        str_folder_name,
        s.get_index_stream_file_name()
    )
