from werkzeug.datastructures import FileStorage
from flask_uploads import UploadSet, IMAGES
from typing import Union
import os

IMAGE_SET = UploadSet("images", IMAGES)


def save_image(image: FileStorage, folder: str = None, name: str = None) -> str:
    """Takes FileStorage and saves it to a folder"""
    return IMAGE_SET.save(image, folder, name)


def get_path(filename: str = None, folder: str = None) -> str:
    """return full path"""
    return IMAGE_SET.path(filename, folder)


def find_image_any_format(filename: str = None, folder: str = None) -> Union[str, None]:
    """returns an image on any of the accepted formats."""
    for _formate in IMAGES:
        image = f"{filename}.{_formate}"
        image_path = IMAGE_SET.path(filename=image, folder=folder)
        if os.path.isfile(image_path):
            return image_path
    return None


# def _retrieve_filename(file: Union[str, FileStorage]):
#     if isinstance(file, FileStorage):
#         return file.filename
#     return file
