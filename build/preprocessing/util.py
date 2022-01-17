from pathlib import Path


def create_dir(tar_path):
    try:
        if not tar_path.exists():
            tar_path.mkdir()
    except(Exception):
        pass


def str2path(path):
    if type(path) == str:
        return Path(path)
    else:
        return path
