# File: archive_handler.py
# Description: Archive file handler methods.
#
# Copyright (c) 2025 Jason Stuber
# Licensed under the MIT License. See the LICENSE file for more details.

from gradhouse.file.file_name import FileName
from gradhouse.file.file_type import FileType

import gzip
import os
import struct
import tarfile


class ArchiveHandler:
    """
    A class to handle archive files.
    """

    _file_extension_map = {
        '.gz': [FileType.FILE_TYPE_ARCHIVE_GZ, FileType.FILE_TYPE_ARCHIVE_TGZ],  # .tar.gz could identify as .gz
        '.tar' : [FileType.FILE_TYPE_ARCHIVE_TAR],
        '.tgz': [FileType.FILE_TYPE_ARCHIVE_TGZ]
    }

    @staticmethod
    def get_file_extension_map() -> dict:
        """
        Get the file extension map.
        :return: dict, dictionary of file extension and a list of associated file types.
        """

        return ArchiveHandler._file_extension_map

    @staticmethod
    def get_file_type_from_extension(file_extension: str) -> list:
        """
        Determine the file type from the file extension.

        :param file_extension: str, file extension
        :return: list, list of file type categories FileType determined by extension.
            If the file type is unknown, return FILE_TYPE_UNKNOWN.
        """

        return ArchiveHandler._file_extension_map.get(file_extension.lower(), [FileType.FILE_TYPE_UNKNOWN])

    @staticmethod
    def get_file_type_from_format(file_path: str) -> FileType:
        """
        Determine the file type from the file format.

        :param file_path: str, path to the file
        :return: FileType, file type determined by the file format.
            If the file type is unknown, return FILE_TYPE_UNKNOWN.
        """

        if ArchiveHandler.is_tar_format(file_path):
            file_type_category = FileType.FILE_TYPE_ARCHIVE_TAR
        elif ArchiveHandler.is_tgz_format(file_path):
            file_type_category = FileType.FILE_TYPE_ARCHIVE_TGZ
        elif ArchiveHandler.is_gzip_format(file_path):
            file_type_category = FileType.FILE_TYPE_ARCHIVE_GZ
        else:
            file_type_category = FileType.FILE_TYPE_UNKNOWN

        return file_type_category

    @staticmethod
    def is_archive_format(file_path:str) -> bool:
        """
         Determine if the file content is in a supported archive format.
         Supported archive formats: tar, tgz, gzip

         :param file_path: str, path to the file
         :return: bool, True if the file is in a supported archive format, False otherwise.

         :raises FileNotFoundError: If the file is not found.
         """

        is_file_found = os.path.isfile(file_path)
        if not is_file_found:
            raise FileNotFoundError('file not found')

        is_tar = ArchiveHandler.is_tar_format(file_path)
        is_tgz = ArchiveHandler.is_tgz_format(file_path)
        is_gzip = ArchiveHandler.is_gzip_format(file_path)

        is_supported = is_tar or is_gzip or is_tgz

        return is_supported

    @staticmethod
    def _is_tar_or_tgz_format(file_path: str) -> bool:
        """
        Determine if the file content is in tar or tgz format.

        :param file_path: str, valid path to the file
        :return: bool, True if the file is in tar or tgz archive format, False otherwise.
        """

        is_tar_file = tarfile.is_tarfile(file_path)

        return is_tar_file

    @staticmethod
    def _is_gzip_or_tgz_format(file_path: str) -> bool:
        """
        Determine if the file content is in gzip or tgz archive format.

        :param file_path: str, valid path to the file
        :return: bool, True if the file is in gzip or tgz archive format, False otherwise.
        """

        is_gzip = True

        with gzip.open(file_path, 'rb') as file_handle:
            try:
                file_handle.read(1)
            except gzip.BadGzipFile:
                is_gzip = False

        return is_gzip

    @staticmethod
    def is_tar_format(file_path: str) -> bool:
        """
        Determine if the file content is in tar archive format.

        :param file_path: str, path to the file
        :return: bool, True if the file is in tar archive format, False otherwise.
                 The method shall raise an exception if the file does not exist or cannot be read.

        :raises FileNotFoundError: If the file is not found.
        """

        is_file_found = os.path.isfile(file_path)
        if not is_file_found:
            raise FileNotFoundError('file not found')

        is_tar_or_tgz_format = ArchiveHandler._is_tar_or_tgz_format(file_path)
        is_gzip_or_tgz_format = ArchiveHandler._is_gzip_or_tgz_format(file_path)

        is_tar_file = is_tar_or_tgz_format and not is_gzip_or_tgz_format

        return is_tar_file

    @staticmethod
    def is_gzip_format(file_path: str) -> bool:
        """
        Determine if the file content is in gzip archive format.

        :param file_path: str, path to the file
        :return: bool, True if the file is in gzip archive format, False otherwise.
                 The method shall raise an exception if the file does not exist or cannot be read.

        :raises FileNotFoundError: If the file is not found.
        """

        is_file_found = os.path.isfile(file_path)
        if not is_file_found:
            raise FileNotFoundError('file not found')

        is_tar_or_tgz_format = ArchiveHandler._is_tar_or_tgz_format(file_path)
        is_gzip_or_tgz_format = ArchiveHandler._is_gzip_or_tgz_format(file_path)

        is_gzip_file = is_gzip_or_tgz_format and not is_tar_or_tgz_format

        return is_gzip_file

    @staticmethod
    def is_tgz_format(file_path: str) -> bool:
        """
        Determine if the file content is in tgz archive format.

        :param file_path: str, path to the file
        :return: bool, True if the file is in tgz archive format, False otherwise.
                 The method shall raise an exception if the file does not exist or cannot be read.

        :raises FileNotFoundError: If the file is not found.
        """

        is_file_found = os.path.isfile(file_path)
        if not is_file_found:
            raise FileNotFoundError('file not found')

        is_tar_or_tgz_format = ArchiveHandler._is_tar_or_tgz_format(file_path)
        is_gzip_or_tgz_format = ArchiveHandler._is_gzip_or_tgz_format(file_path)

        is_tgz_file = is_gzip_or_tgz_format and is_tar_or_tgz_format

        return is_tgz_file

    @staticmethod
    def list_contents(file_path: str) -> list[str]:
        """
        List the files contained in a supported archive file.

        :param file_path: str, path to the archive file
        :return: list[str], list of the files in the archive.

        :raises TypeError: If the file is not a supported archive format.
        :raises TypeError: If the source file is not a supported archive format in the list.
        """

        is_archive_file = ArchiveHandler.is_archive_format(file_path)
        if not is_archive_file:
            raise TypeError('file not a supported archive format')

        if ArchiveHandler.is_gzip_format(file_path):
            file_list = ArchiveHandler._list_gzip_contents(file_path)
        elif ArchiveHandler.is_tar_format(file_path):
            file_list = ArchiveHandler._list_tar_contents(file_path)
        elif ArchiveHandler.is_tgz_format(file_path):
            file_list = ArchiveHandler._list_tgz_contents(file_path)
        else:
            raise TypeError('file not listed as a supported archive format')

        return file_list

    @staticmethod
    def _list_tar_or_tgz_contents(file_path: str) -> list[str]:
        """
        List the files contained in a tar or tgz archive file.

        :param file_path: str, path to a valid tar or tgz archive file
        :return: list[str], list of the files in the tar or tgz archive.
        """

        file_list = []

        with tarfile.open(file_path, 'r') as tar_handle:
            for member in tar_handle.getmembers():
                if member.isfile():
                    file_list.append(member.name)

        return file_list

    @staticmethod
    def _list_tar_contents(file_path: str) -> list[str]:
        """
        List the files contained in a tar archive file.

        :param file_path: str, path to the tar archive file
        :return: list[str], list of the files in the tar archive.

        :raises FileNotFoundError: If the file is not found.
        :raises TypeError: If the file is not in tar format.
        """

        is_file_found = os.path.isfile(file_path)
        if not is_file_found:
            raise FileNotFoundError('file not found')

        is_file_tar_format = ArchiveHandler.is_tar_format(file_path)
        if not is_file_tar_format:
            raise TypeError('file not in tar format')

        file_list = ArchiveHandler._list_tar_or_tgz_contents(file_path)

        return file_list

    @staticmethod
    def _list_tgz_contents(file_path: str) -> list[str]:
        """
        List the files contained in a tgz tar.gz archive file.

        :param file_path: str, path to the tgz archive file
        :return: list[str], list of the files in the tgz archive.

        :raises FileNotFoundError: If the file is not found.
        :raises TypeError: If the file is not in tgz format.
        """

        is_file_found = os.path.isfile(file_path)
        if not is_file_found:
            raise FileNotFoundError('file not found')

        is_file_tgz_format = ArchiveHandler.is_tgz_format(file_path)
        if not is_file_tgz_format:
            raise TypeError('file not in tgz format')

        file_list = ArchiveHandler._list_tar_or_tgz_contents(file_path)

        return file_list

    @staticmethod
    def _list_gzip_contents(file_path: str) -> list[str]:
        """
        List the files contained in a gzip archive file.
        :param file_path: str, path to the gzip file
        :return: list[str], list of the files in the gzip archive.

        :raises FileNotFoundError: If the file is not found.
        :raises TypeError: If the file is not in gzip format.
        """

        is_file_found = os.path.isfile(file_path)
        if not is_file_found:
            raise FileNotFoundError('file not found')

        is_file_gzip_format = ArchiveHandler.is_gzip_format(file_path)
        if not is_file_gzip_format:
            raise TypeError('file not in gzip format')

        file_list = []

        with open(file_path, 'rb') as file_handle:
            id1, id2, compression, flags, mtime, extra_flags, os_id = struct.unpack('<BBBBLBB',
                                                                                    file_handle.read(10))
            is_valid_compression_format = (id1 == 0x1F and id2 == 0x8B and compression == 0x08)
            if is_valid_compression_format:
                is_extra_field_present = (flags & (1 << 2) != 0)
                if is_extra_field_present:
                    file_handle.read(struct.unpack('<H', file_handle.read(2))[0])

                is_filename_field_present = (flags & (1 << 3) != 0)
                if is_filename_field_present:
                    name = b''.join(iter(lambda: file_handle.read(1), b'\0'))
                    name = name.decode()
                    file_list.append(name)

        return file_list

    @staticmethod
    def is_extract_possible(source_file_path: str, destination_directory: str) -> bool:
        """
        Indicator method to check that the archive extraction is to a valid location, the contents filenames are not
        forbidden, and that the destination directory exists and the extracted files will not overwrite an existing
        filename.

        :param source_file_path: str, path to the archive file
        :param destination_directory: str, path to the destination directory
            This method checks that the extraction of the archive contents into this directory is safe.
        :returns: bool, True if the extraction is possible, False if extraction is forbidden.
        """

        error_log = []
        is_file_found = os.path.isfile(source_file_path)
        if not is_file_found:
            error_log.append('file not found')

        is_directory = os.path.isdir(destination_directory)
        if not is_directory:
            error_log.append('destination directory not found')

        if is_file_found and is_directory:
            file_contents = ArchiveHandler.list_contents(source_file_path)

            is_unique_names = FileName.is_filename_list_unique(file_contents, is_case_insensitive=True,
                                                               is_filename_only=False)
            if not is_unique_names:
                error_log.append('archive contents filename is not unique on case-insensitive file systems')

            is_valid_filenames = all([FileName.is_filename_allowed(entry) for entry in file_contents])
            if not is_valid_filenames:
                error_log.append('archive contents filenames are forbidden')

            if is_unique_names and is_valid_filenames:
                for contents_filename in file_contents:
                    destination_filename = os.path.join(destination_directory, contents_filename)
                    is_destination_file_found = os.path.isfile(destination_filename)
                    if is_destination_file_found:
                        error_log.append('destination file already exists')
                        break

        is_possible = len(error_log) == 0
        return is_possible

    @staticmethod
    def _extract_gzip_contents_private(source_file_path: str, destination_directory:str) -> None:
        """
        Extract the contents of a gzip archive file to a specified path.
        This method assumes the source file is a gzip archive and that is_extract_possible has been before.

        :param source_file_path: str, path to the gzip archive file
        :param destination_directory: str, path to the destination directory
            The archive contents will be extracted into this directory.

        :raises IOError: If the source file cannot be read.
        :raises FileExistsError: If the destination directory already exists.
        :raises IOError: If the destination file cannot be written.
        """

        with gzip.open(source_file_path, 'rb') as file_handle:
            try:
                buffer = file_handle.read()
            except IOError:
                raise IOError('file could not be read')
            finally:
                file_handle.close()

        file_contents = ArchiveHandler.list_contents(source_file_path)
        for contents_filename in file_contents:
            destination_filename = os.path.join(destination_directory, contents_filename)
            with open(destination_filename, 'wb') as file_handle:
                file_handle.write(buffer)
                file_handle.close()

    @staticmethod
    def _extract_tar_or_tgz_contents_private(source_file_path: str, destination_directory:str) -> None:
        """
        Extract the contents of a tar or tgz archive file to a specified path.
        This method assumes the source file is a tar or tgz archive and that is_extract_possible has been called.

        :param source_file_path: str, path to the tar or tgz archive file
        :param destination_directory: str, path to the destination directory
            The archive contents will be extracted into this directory.
        """

        with tarfile.open(source_file_path, 'r') as tar:
            file_members = [member for member in tar.getmembers() if member.isfile()]
            for member in file_members:
                tar.extract(member, destination_directory)

    @staticmethod
    def extract_gzip_contents(source_file_path: str,
                              destination_directory: str) -> None:
        """
        Extract the contents of a gzip archive file to a specified path.

        :param source_file_path: str, path to the gzip archive file
        :param destination_directory: str, path to the destination directory
            The archive contents will be extracted into this directory.

        :raises TypeError: If the source file is not in gzip archive format.
        :raises ValueError: If the extraction is not possible.
            This can occur for several reasons such as source file, destination directory or archive contents.
        """

        is_gzip = ArchiveHandler.is_gzip_format(source_file_path)
        if not is_gzip:
            raise TypeError('file not in gzip archive format')

        is_possible = ArchiveHandler.is_extract_possible(source_file_path, destination_directory)
        if not is_possible:
            raise ValueError('extraction not possible')

        ArchiveHandler._extract_gzip_contents_private(source_file_path, destination_directory)

    @staticmethod
    def extract_tar_contents(source_file_path: str,
                             destination_directory: str) -> None:
        """
        Extract the contents of a tar archive file to a specified path.

        :param source_file_path: str, path to the tar archive file
        :param destination_directory: str, path to the destination directory
            The archive contents will be extracted into this directory.

        :raises TypeError: If the source file is not in tar archive format.
        :raises ValueError: If the extraction is not possible.
            This can occur for several reasons such as source file, destination directory or archive contents.
        """

        is_tar = ArchiveHandler.is_tar_format(source_file_path)
        if not is_tar:
            raise TypeError('file not in tar archive format')

        is_possible = ArchiveHandler.is_extract_possible(source_file_path, destination_directory)
        if not is_possible:
            raise ValueError('extraction not possible')

        ArchiveHandler._extract_tar_or_tgz_contents_private(source_file_path, destination_directory)

    @staticmethod
    def extract_tgz_contents(source_file_path: str,
                             destination_directory: str) -> None:
        """
        Extract the contents of a tgz archive file to a specified path.

        :param source_file_path: str, path to the tgz archive file
        :param destination_directory: str, path to the destination directory
            The archive contents will be extracted into this directory.

        :raises TypeError: If the source file is not in tgz archive format.
        :raises ValueError: If the extraction is not possible.
            This can occur for several reasons such as source file, destination directory or archive contents.
        """

        is_tgz = ArchiveHandler.is_tgz_format(source_file_path)
        if not is_tgz:
            raise TypeError('file not in tgz archive format')

        is_possible = ArchiveHandler.is_extract_possible(source_file_path, destination_directory)
        if not is_possible:
            raise ValueError('extraction not possible')

        ArchiveHandler._extract_tar_or_tgz_contents_private(source_file_path, destination_directory)

    @staticmethod
    def extract_contents(source_file_path: str, destination_directory: str):
        """
        Extract the contents of an archive file to a specified path.

        :param source_file_path: str, path to the archive file
        :param destination_directory: str, path to the destination directory

        :raises TypeError: If the source file is not a supported archive format.
        :raises TypeError: If the source file is not a supported archive format in the list.
        """

        is_archive_file = ArchiveHandler.is_archive_format(source_file_path)
        if not is_archive_file:
            raise TypeError('file not a supported archive format')

        if  ArchiveHandler.is_gzip_format(source_file_path):
            ArchiveHandler.extract_gzip_contents(source_file_path, destination_directory)
        elif ArchiveHandler.is_tar_format(source_file_path):
            ArchiveHandler.extract_tar_contents(source_file_path, destination_directory)
        elif ArchiveHandler.is_tgz_format(source_file_path):
            ArchiveHandler.extract_tgz_contents(source_file_path, destination_directory)
        else:
            raise TypeError('file not listed as a supported archive format')
