# File: file_handler.py
# Description: File methods.
#
# Copyright (c) 2025 Jason Stuber
# Licensed under the MIT License. See the LICENSE file for more details.

from gradhouse.file.hash_service import HashType, HashService
from gradhouse.file.file_name import FileName
from gradhouse.file.file_system import FileSystem
from gradhouse.file.file_type import FileType

from gradhouse.file.handler.archive_handler import ArchiveHandler
from gradhouse.file.handler.image_handler import ImageHandler
from gradhouse.file.handler.pdf_handler import PdfHandler
from gradhouse.file.handler.postscript_handler import PostscriptHandler
from gradhouse.file.handler.tex_handler import TexHandler
from gradhouse.file.handler.xml_handler import XmlHandler


class FileHandler:
    """
    File handler methods
    """

    _file_handlers = [ArchiveHandler(), ImageHandler(), PdfHandler(), PostscriptHandler(), TexHandler(), XmlHandler()]

    @staticmethod
    def get_metadata(file_path: str, hash_types: list[HashType]) -> dict:
        """
        Get the metadata of a file.

        The metadata includes:
            - base file name
            - file size
            - timestamp (last modified)
            - hash

        :param file_path: str, path to the file
        :param hash_types: list, set of hash types of type HashType,
            such as [HashType.HASH_TYPE_MD5, HashType.HASH_TYPE_SHA256]
        :return: dict, dictionary containing the metadata

        :raises FileNotFoundError: If the file is not found.
        """

        if not FileSystem.is_file(file_path):
            raise FileNotFoundError('file not found')

        metadata = dict()

        metadata['filename'] = FileName.get_file_basename(file_path)
        metadata['size_bytes'] = FileSystem.get_file_size(file_path)
        metadata['hash'] = {}
        for hash_type in hash_types:
            metadata['hash'][hash_type.value] = HashService.calculate_file_hash(file_path, hash_type)
        metadata['timestamp_iso'] = FileSystem.get_file_timestamp(file_path)
        metadata['file_type'] = FileHandler.get_file_type_from_format(file_path).value

        return metadata

    @staticmethod
    def get_file_type_from_extension(file_path: str) -> list[FileType]:
        """
        Get the file type category from the extension of the file path.

        :param file_path: str, file path
        :return: list[FileType], list of matching file type category
            If the file extension is not found, then an empty list will be returned.
        """

        file_extension = FileName.get_file_extension(file_path).lower()
        file_category_list = FileHandler._get_file_type_using_extension(file_extension)

        return file_category_list

    @staticmethod
    def get_file_type_from_format(file_path: str, use_extension: bool = True) -> FileType:
        """
        Determine the file type from the file format.

        :param file_path: str, path to the file
        :param use_extension: bool, whether to use file extension to determine the potential handlers or not.
        :return: FileType, file type determined by the file format.
            If the file type is unknown, return FILE_TYPE_UNKNOWN.

        :raises FileNotFoundError: If the file is not found.
        """

        is_file_found = FileSystem.is_file(file_path)
        if not is_file_found:
            raise FileNotFoundError('file not found')

        if use_extension:
            file_extension = FileName.get_file_extension(file_path).lower()
            file_handler_list = FileHandler._get_file_handlers_from_extension(file_extension)
        else:
            file_handler_list = FileHandler._get_file_handlers()

        file_type = FileType.FILE_TYPE_UNKNOWN
        for file_handler in file_handler_list:
            file_type = file_handler.get_file_type_from_format(file_path)
            if file_type != FileType.FILE_TYPE_UNKNOWN:
                # non-trivial file type detected
                break

        return file_type

    @staticmethod
    def _get_file_type_using_extension(file_extension: str) -> list[FileType]:
        """
        Get the file type category from the file extension.
        :param file_extension: str, file extension
        :return: list[FileType], list of matching file type category
            If the file extension is not found, then an empty list will be returned.
        """

        file_category_list = []

        if len(file_extension) > 0:
            file_handler_list = FileHandler._get_file_handlers_from_extension(file_extension.lower())
            for file_handler in file_handler_list:
                file_type_list = file_handler.get_file_type_from_extension(file_extension)
                file_category_list.extend(file_type_list)

        return file_category_list

    @staticmethod
    def _get_file_handlers() -> list:
        """
        Return a list of file handlers.
        :return: list, list of file handlers

        :raises ValueError: If the handler does not have a callable get_file_extension_map
        """

        for handler in FileHandler._file_handlers:
            if not hasattr(handler, 'get_file_extension_map') or not callable(handler.get_file_extension_map):
                raise ValueError("Handler must have a callable 'get_file_extension_map' method.")

        return FileHandler._file_handlers

    @staticmethod
    def _get_file_handlers_from_extension(extension: str)->list:
        """
        Class method to get a list of file handlers based on the file extension.

        :param extension: str, file extension. This is '.tex' for a TeX file for example
        :return: list, list of file handlers that are associated with the extension.
            If no file handlers are associated with the extension, an empty list is returned.

        :raises ValueError: If the handler does not have a callable 'get_file_extension_map' method.
        """

        file_extension_to_handler_map = dict()

        file_handler_list = FileHandler._get_file_handlers()

        for handler in file_handler_list:
            for ext in handler.get_file_extension_map():
                ext = ext.lower()
                if ext not in file_extension_to_handler_map:
                    file_extension_to_handler_map[ext] = []
                # Ensure the handler is not already in the list for this extension
                if handler not in file_extension_to_handler_map[ext]:
                    file_extension_to_handler_map[ext].append(handler)

        found_file_handlers = file_extension_to_handler_map.get(extension.lower(), [])
        return found_file_handlers
