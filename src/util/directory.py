"""
Methods to interact os directory skills
"""
import os
import shutil

def is_dir(path):
    """ Verify if this dir exist """
    return os.path.isdir(path)

def join_path(parent_path, path):
    """ Method to make a directory to keep streaming files from a camera. """
    return os.path.join(parent_path, path)

def make_dir(path):
    """ Method to create a dir """
    os.mkdir(path)

def delete_dir(path):
    """ Method to delete a directory that keep streaimg files. """
    try:
        shutil.rmtree(path)
    except OSError as error:
        print(f"Error deleting: {error.filename} - {error.strerror}.")

def get_root_path():
    """ Method to get current current work dir from caller. """
    # os.chdir('..')
    return os.getcwd()

def go_up():
    """
    Method to go up on the directory
    """
    os.chdir('..')

def get_list_files(directory):
    # files=os.listdir(directory)
    # for i in range(len(files)):
    #     files[i] = join_path(directory, files[i])
    return [join_path(directory, file) for file in os.listdir(directory)]
