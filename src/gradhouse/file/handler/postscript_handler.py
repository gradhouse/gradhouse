# File: postscript_handler.py
# Description: Postscript (PS) file handler methods
#
# Copyright (c) 2025 Jason Stuber
# Licensed under the MIT License. See the LICENSE file for more details.

import os

from gradhouse.file.file_type import FileType


class PostscriptHandler:
    """
    A class to handle postscript (PS) files.
    """

    _file_extension_map = {
        '.ps' : [FileType.FILE_TYPE_POSTSCRIPT_PS],
        '.eps': [FileType.FILE_TYPE_POSTSCRIPT_EPS],
        '.epsf': [FileType.FILE_TYPE_POSTSCRIPT_EPSF],
        '.epsi': [FileType.FILE_TYPE_POSTSCRIPT_EPSI]
    }

    @staticmethod
    def get_file_extension_map() -> dict:
        """
        Get the file extension map.
        :return: dict, dictionary of file extension and a list of associated file types.
        """

        return PostscriptHandler._file_extension_map

    @staticmethod
    def get_file_type_from_extension(file_extension: str) -> list:
        """
        Determine the file type from the file extension.

        :param file_extension: str, file extension
        :return: list, list of file type categories FileType determined by extension.
            If the file type is unknown, return FILE_TYPE_UNKNOWN.
        """

        return PostscriptHandler._file_extension_map.get(file_extension.lower(), [FileType.FILE_TYPE_UNKNOWN])

    @staticmethod
    def get_file_type_from_format(file_path: str) -> FileType:
        """
        Determine the file type from the file format.

        The current implementation does not distinguish between different postscript formats.

        :param file_path: str, path to the file
        :return: FileType, file type determined by the file format.
            If the file type is unknown, return FILE_TYPE_UNKNOWN.
        """

        is_postscript = PostscriptHandler.is_postscript_format(file_path)
        if is_postscript:
            file_type_category = FileType.FILE_TYPE_POSTSCRIPT_PS
        else:
            file_type_category = FileType.FILE_TYPE_UNKNOWN

        return file_type_category

    @staticmethod
    def is_postscript_format(file_path: str) -> bool:
        """
        Determine if the file context is in postscript format.

        :param file_path: str, path to the file
        :return: bool, True if the file is in postscript format, False otherwise.
                 The method shall raise an exception if the file does not exist or cannot be read.

        :raises FileNotFoundError: If the file is not found.
        """

        postscript_headers = [
            "%!PostScript",
            "%!PS-Adobe-3.0",
            "%!PS-Adobe-2.0",
            "%!PS-Adobe-1.0"
        ]

        is_file_found = os.path.isfile(file_path)
        if not is_file_found:
            raise FileNotFoundError('file not found')

        is_postscript_file = False
        try:
            with open(file_path, 'r') as file:
                first_line = file.readline().strip()
                is_postscript_file = any(first_line.startswith(header) for header in postscript_headers)
        except Exception as e:
            print(f"Error reading file: {e}")
            return is_postscript_file

        return is_postscript_file
