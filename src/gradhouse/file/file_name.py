# File: file_name.py
# Description: Filename methods.
#
# Copyright (c) 2025 Jason Stuber
# Licensed under the MIT License. See the LICENSE file for more details.

import os
import re


class FileName:
    """
    Filename methods
    """

    MAX_FILENAME_LENGTH = 250

    @staticmethod
    def get_file_extension(file_path: str) -> str:
        """
        Get the file extension from the file path.

        :param file_path: str, path to the file
        :return: str, file extension
        """

        return os.path.splitext(file_path)[1]

    @staticmethod
    def get_file_basename(file_path: str) -> str:
        """
        Get the file basename from the file path.
        For /d/directory1/directory2/filename.txt, this is filename.txt.

        :param file_path: str, path to the file
        :return: str, file basename
        """

        base_name = os.path.basename(file_path)

        return base_name

    @staticmethod
    def is_path_characters_allowed(file_path: str) -> bool:
        """
        Determine if the file path has only allowed characters.
        Allowed characters are alphanumeric, underscore, periods, plus, minus and equals.

        :param file_path: str, path to the file
        :return: bool, True if the file path has only allowed characters, False otherwise.
        """

        allowed_pattern = re.compile(r'^[\w\-.+=]+$')

        # Split the path into components, linux style
        components = file_path.split('/')

        return all(allowed_pattern.match(component) and component not in ('', '.', '..')
                         for component in components)

    @staticmethod
    def is_path_within_directory(base_directory: str, target_path: str) -> bool:
        """
        Check if the target path is within the specified base directory.

        This function ensures that the target path is a subdirectory or file within the given base directory,
        preventing directory traversal attacks by verifying that the target path does not escape the base directory.

        :param base_directory: str, the base directory path
        :param target_path: str, the target path to check
        :return: bool, True if the target path is within the base directory, False otherwise.
        """

        # Normalize and resolve absolute paths
        abs_base_directory = os.path.abspath(os.path.normpath(base_directory))
        abs_target_path = os.path.abspath(os.path.normpath(target_path))

        # Check if the target path is within the base directory
        return os.path.commonpath([abs_base_directory]) == os.path.commonpath([abs_base_directory, abs_target_path])

    @staticmethod
    def is_filename_allowed(file_path: str) -> bool:
        """
        Determine if the filename is allowed on a Linux-style filesystem.
        A filename is considered allowed if:
        - It contains only valid characters (alphanumeric, underscore, periods, plus, minus, equals).
        - It does not allow directory traversal attacks.
        - It is within the maximum allowed length.

        :param file_path: str, path to the file (relative path expected).
        :return: bool, True if the filename is allowed (safe), False otherwise.
        """

        # Check if the file path could contain traversal attacks
        temp_path = os.path.join('temp', file_path)
        is_within_temp_directory = FileName.is_path_within_directory('temp', temp_path)

        # Check if the file path has only allowed characters
        has_valid_characters = FileName.is_path_characters_allowed(file_path)

        # Check if the file path length is within limits
        n = len(file_path)
        is_length_valid = (0 < n) and (n < FileName.MAX_FILENAME_LENGTH)

        return is_within_temp_directory and has_valid_characters and is_length_valid

    @staticmethod
    def is_filename_list_unique(filename_list: list[str], is_case_insensitive: bool=True,
                                is_filename_only: bool=False) -> bool:
        """
        Determines if a filename list has unique entries for case-insensitive file systems or relative directories.

        :param filename_list: list[str], list of filenames
        :param is_case_insensitive: bool, if True then the method checks that the filenames are unique even on
            case-insensitive filesystems such as Windows. If False then this check will be skipped. Default True.
        :param is_filename_only: bool, if True then the method tests that the base filenames are unique, without
            the directory path. If False then this check will be skipped. Default False.

        :return: bool, True if the filenames are unique, otherwise False
        """

        # Process filenames based on flags
        processed_filenames = [
            FileName.get_file_basename(filename) if is_filename_only else filename
            for filename in filename_list
        ]
        if is_case_insensitive:
            processed_filenames = [filename.lower() for filename in processed_filenames]

        return len(set(processed_filenames)) == len(processed_filenames)
