import os
import shutil

def make_dir(parent_path, folder_name):
    """
    Method to make a directory to keep streaming files from a camera
    """
    path = os.path.join(parent_path, folder_name)
    os.mkdir(path)
    return path
    
def delete_dir(path):
    """
    Method to delete a directory that keep streaimg files
    """
    try:
        shutil.rmtree(path)
    except OSError as e:
        print(f"Error deleting: {e.filename} - {e.strerror}.")