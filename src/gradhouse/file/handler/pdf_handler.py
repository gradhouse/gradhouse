# File: pdf_handler.py
# Description: Portable document format (PDF) file handler methods.
#
# Copyright (c) 2025 Jason Stuber
# Licensed under the MIT License. See the LICENSE file for more details.


import os

from gradhouse.file.file_system import FileSystem
from gradhouse.file.file_type import FileType


class PdfHandler:
    """
    A class to handle portable document format (PDF) files.
    """

    _file_extension_map = {
        '.pdf': [FileType.FILE_TYPE_PDF]
    }

    @staticmethod
    def get_file_extension_map() -> dict:
        """
        Get the file extension map.
        :return: dict, dictionary of file extension and a list of associated file types.
        """

        return PdfHandler._file_extension_map

    @staticmethod
    def get_file_type_from_extension(file_extension: str) -> list:
        """
        Determine the file type from the file extension.

        :param file_extension: str, file extension
        :return: list, list of file type categories FileType determined by extension.
            If the file type is unknown, return FILE_TYPE_UNKNOWN.
        """

        return PdfHandler._file_extension_map.get(file_extension.lower(), [FileType.FILE_TYPE_UNKNOWN])

    @staticmethod
    def get_file_type_from_format(file_path: str) -> FileType:
        """
        Determine the file type from the file format.

        :param file_path: str, path to the file
        :return: FileType, file type determined by the file format.
            If the file type is unknown, return FILE_TYPE_UNKNOWN.
        """

        is_pdf = PdfHandler.is_pdf_format(file_path)
        if is_pdf:
            file_type_category = FileType.FILE_TYPE_PDF
        else:
            file_type_category = FileType.FILE_TYPE_UNKNOWN

        return file_type_category

    @staticmethod
    def is_pdf_format(file_path: str) -> bool:
        """
        Determine if the file content is in portable document format (PDF) format.

        :param file_path: str, path to the file
        :return: bool, True if the file is in PDF format, False otherwise.
                 The method shall raise an exception if the file does not exist or cannot be read.

        :raises FileNotFoundError: If the file is not found.
        """

        is_file_found = FileSystem.is_file(file_path)
        if not is_file_found:
            raise FileNotFoundError('file not found')

        is_pdf_file = False

        with open(file_path, 'rb') as file:
            header = file.read(5)
            if header == b'%PDF-':
                is_pdf_file = True

        return is_pdf_file
