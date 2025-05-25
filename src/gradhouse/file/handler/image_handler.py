# File: image_handler.py
# Description: Image handler methods.
#
# Copyright (c) 2025 Jason Stuber
# Licensed under the MIT License. See the LICENSE file for more details.

import os
from PIL import Image

from gradhouse.file.file_type import FileType


class ImageHandler:
    """
    A class to handle image files.
    """

    _file_extension_map = {
        '.bmp': [FileType.FILE_TYPE_IMAGE_BMP],
        '.gif': [FileType.FILE_TYPE_IMAGE_GIF],
        '.ico': [FileType.FILE_TYPE_IMAGE_ICO],
        '.jpeg': [FileType.FILE_TYPE_IMAGE_JPG],
        '.jpg': [FileType.FILE_TYPE_IMAGE_JPG],
        '.png': [FileType.FILE_TYPE_IMAGE_PNG],
        '.tif': [FileType.FILE_TYPE_IMAGE_TIFF],
        '.tiff': [FileType.FILE_TYPE_IMAGE_TIFF],
    }

    pil_to_type_map = {
        'BMP': FileType.FILE_TYPE_IMAGE_BMP,
        'GIF': FileType.FILE_TYPE_IMAGE_GIF,
        'ICO': FileType.FILE_TYPE_IMAGE_ICO,
        'PNG': FileType.FILE_TYPE_IMAGE_PNG,
        'JPEG': FileType.FILE_TYPE_IMAGE_JPG,
        'TIFF': FileType.FILE_TYPE_IMAGE_TIFF
    }

    @staticmethod
    def get_file_extension_map() -> dict:
        """
        Get the file extension map.
        :return: dict, dictionary of file extension and a list of associated file types.
        """

        return ImageHandler._file_extension_map

    @staticmethod
    def get_file_type_from_extension(file_extension: str) -> list:
        """
        Determine the file type from the file extension.

        :param file_extension: str, file extension
        :return: list, list of file type categories FileType determined by extension.
            If the file type is unknown, return FILE_TYPE_UNKNOWN.
        """
        return ImageHandler._file_extension_map.get(file_extension.lower(), [FileType.FILE_TYPE_UNKNOWN])

    @staticmethod
    def get_file_type_from_format(file_path: str) -> FileType:
        """
        Determine the file type from the file format.

        Method currently not implemented.

        :param file_path: str, path to the file
        :return: FileType, file type determined by the file format.
            If the file type is unknown, return FILE_TYPE_UNKNOWN.

        :raises FileNotFoundError: If the file is not found.
        :raises IOError: If the file cannot be opened or read.
        """

        is_file_found = os.path.isfile(file_path)
        if not is_file_found:
            raise FileNotFoundError('file not found')

        try:
            with Image.open(file_path) as img:
                file_type_category = ImageHandler.pil_to_type_map.get(img.format, FileType.FILE_TYPE_UNKNOWN)

        except IOError:
            file_type_category = FileType.FILE_TYPE_UNKNOWN

        return file_type_category
