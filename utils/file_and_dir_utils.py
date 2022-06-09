import os


def create_dir_if_not_exist(dir_name):
    if not os.path.isdir(dir_name):
        os.makedirs(dir_name)
    return dir_name
