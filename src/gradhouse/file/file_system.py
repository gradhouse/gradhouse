# File: file_system.py
# Description: File system operatopms.
#
# Copyright (c) 2025 Jason Stuber
# Licensed under the MIT License. See the LICENSE file for more details.

from datetime import datetime, timezone
import os
import shutil


class FileSystem:
    """
    File system operations
    """

    @staticmethod
    def is_file(file_path: str) -> bool:
        """
        Determine if the given path corresponds to an existing file.

        :param file_path: str, path to the file
        :return: bool, True if the path corresponds to a file, False otherwise.
                 If the object is found but does not correspond to a file, False is also returned.
        """

        is_file_found = os.path.isfile(file_path)
        return is_file_found

    @staticmethod
    def is_directory(directory_path: str) -> bool:
        """
        Determine if the given path corresponds to an existing directory.

        :param directory_path: str, path to the directory
        :return: bool, True if the path corresponds to an existing directory, False otherwise.
                 If the object is found but does not correspond to a directory, False is also returned.
        """

        is_directory_found = os.path.isdir(directory_path)
        return is_directory_found

    @staticmethod
    def is_object(path: str) -> bool:
        """
        Determine if the given path corresponds to an existing file system object.

        :param path: str, path to a file system object, such as a file or directory
        :return: bool, True if the path corresponds to an existing file system object, False otherwise.
        """

        is_present = os.path.exists(path)
        return is_present

    @staticmethod
    def get_file_size(file_path: str) -> int:
        """
        Determines the file size in bytes.

        :param file_path: str, path to the file
        :return: int, size of the file in bytes.

        :raises FileNotFoundError: If the file is not found.
        """

        is_file_found = FileSystem.is_file(file_path)
        if not is_file_found:
            raise FileNotFoundError('file not found')

        file_size = os.path.getsize(file_path)

        return file_size

    @staticmethod
    def create_directory(directory_path: str) -> None:
        """
        Create a directory.

        :param directory_path: str, path to the directory

        :raises FileExistsError: If the file system object already exists.
        :raises OSError: If the directory could not be created.
        """

        is_present = FileSystem.is_object(directory_path)
        if is_present:
            raise FileExistsError('file system object already exists')

        try:
            os.makedirs(directory_path, exist_ok=False)
        except OSError as exception_msg:
            raise OSError(f"An error occurred while creating the directory: {exception_msg}")

    @staticmethod
    def remove_directory(directory_path: str) -> None:
        """
        Remove the directory and its contents.

        :param directory_path: str, path to the directory

        :raises FileNotFoundError: If the directory does not exist or is not a directory.
        :raises OSError: If the directory could not be removed.
        """

        is_dir = FileSystem.is_directory(directory_path)
        if not is_dir:
            raise FileNotFoundError('path does not exist or is not a directory')

        try:
            shutil.rmtree(directory_path)
        except OSError as exception_msg:
            raise OSError(f"An error occurred while deleting the directory: {exception_msg}")

    @staticmethod
    def get_file_timestamp(file_path: str) -> str:
        """
        Determines the timestamp when the file was last modified.

        :param file_path: str, path to the file
        :return: str, timestamp when the file was last modified in ISO 8601 format.

        :raises FileNotFoundError: If the file is not found.
        """

        is_file_found = FileSystem.is_file(file_path)
        if not is_file_found:
            raise FileNotFoundError('file not found')

        last_modified_timestamp_seconds = int(os.stat(file_path).st_mtime)
        timestamp_iso = datetime.fromtimestamp(last_modified_timestamp_seconds, timezone.utc).isoformat()

        return timestamp_iso

    @staticmethod
    def is_utf8_encoded(file_path: str) -> bool:
        """
        Determine if the file is UTF-8 encoded.

        :param file_path: str, path to the file
        :return: bool, True if the file is UTF-8 encoded, otherwise False

        :raises FileNotFoundError: If the file is not found.
        """

        is_file_found = FileSystem.is_file(file_path)
        if not is_file_found:
            raise FileNotFoundError('file not found')

        try:
            with open(file_path, 'rb') as file:
                raw_data = file.read()
                raw_data.decode('utf-8')
            is_utf8 = True
        except UnicodeDecodeError:
            is_utf8 = False

        return is_utf8


    @staticmethod
    def list_files(directory_path: str, include_subdirectories: bool=False) -> list[str]:
        """
        List all filenames in a specified directory.

        :param directory_path: str, path to the directory
        :param include_subdirectories: bool, if True then lists all filenames from subdirectories, defaults to False
        :return: list of str, list of filenames in the specified directory, relative to the directory

        :raises FileNotFoundError: If the directory is not found.
        """

        is_valid_directory = FileSystem.is_directory(directory_path)
        if not is_valid_directory:
            raise FileNotFoundError(f"The directory {directory_path} does not exist.")

        filename_list = []
        if include_subdirectories:
            for root, _, files in os.walk(directory_path):
                for file in files:
                    full_path = os.path.join(root, file)
                    relative_path = os.path.relpath(full_path, directory_path)
                    filename_list.append(relative_path)
        else:
            filename_list = [f for f in os.listdir(directory_path) if FileSystem.is_file(os.path.join(directory_path, f))]

        return filename_list
