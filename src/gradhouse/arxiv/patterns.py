# File: patterns.py
# Description: Methods for parsing and validating arXiv filenames and generating related URLs.
#
# Copyright (c) 2025 Jason Stuber
# Licensed under the MIT License. See the LICENSE file for more details.
#
# Disclaimer:
# This software is not affiliated with, endorsed by, or sponsored by arXiv, Cornell University, or any of their affiliates.
# All arXiv data, logos, and trademarks are the property of their respective owners.
# Users of this software are solely responsible for ensuring their use of arXiv data complies with arXiv's policies and terms.
# For more information, see:
# - https://arxiv.org/help/license
# - https://info.arxiv.org/help/bulk_data_s3.html

import os
import re

from gradhouse.file.file_handler import FileHandler
from gradhouse.file.file_name import FileName
from gradhouse.file.file_system import FileSystem
from gradhouse.file.file_type import FileType
from gradhouse.file.handler.archive_handler import ArchiveHandler

class Patterns:
    """
    This class contains static methods for parsing, validating, and constructing information related to arXiv bulk
    archive and submission filenames. It includes utilities to extract metadata from filenames, check filename
    patterns, and generate URLs and S3 URIs for arXiv resources.
    """

    @staticmethod
    def parse_bulk_archive_filename(filename: str) -> tuple[str, str, str] | None:
        """
        Extract the year, month, and sequence number from a bulk archive filename.

        Bulk archive filenames follow the format: arXiv_src_{yymm}_{seq_num}.tar
        - yy: last two digits of the year (e.g., '99' for 1999)
        - mm: two-digit month number (e.g., '02' for February)
        - seq_num: three-digit sequence number within the month (e.g., '005' for the fifth file)        

        For example: arXiv_src_9902_005.tar -> ('99', '02', '005')

        :param filename: str, the bulk archive filename
        :return: tuple[str, str, str] or None, (yy, mm, seq_num) if the filename matches the pattern.
            If the filename does not match the pattern then None is returned.
        """

        basename = FileName.get_file_basename(filename)
        match = re.match(r'^arXiv_src_(\d{2})(\d{2})_(\d{3})\.tar$', basename)
        result = None
        if match:
            result = match.groups()
        return result

    @staticmethod
    def is_bulk_archive_filename(filename: str) -> bool:
        """
        Determine if the given filename is a valid arXiv bulk archive filename.

        A valid bulk archive filename must:
        - Match the pattern 'arXiv_src_{yymm}_{seq_num}.tar'
        - Have a two-digit month (mm) in the range '01' to '12'

        :param filename: str, the filename to check (can include a path)
        :return: bool, True if the filename matches the bulk archive pattern and has a valid month, False otherwise
        """
        result = False
        parts = Patterns.parse_bulk_archive_filename(filename)
        if parts:
            _, mm, _ = parts
            if mm.isdigit() and 1 <= int(mm) <= 12:
                result = True
        return result

    @staticmethod
    def generate_uri_for_bulk_archive_filename(filename: str) -> str:
        """
        Generate the bulk archive Uniform Resource Identifier (URI) for the given arXiv bulk archive filename.
        The filename should follow the bulk archive file naming scheme.

        The base name of the filename is determined and the URI generated. For example
            local_directory/arXiv_src_9902_005.tar generates the URI 's3://arxiv/src/arXiv_src_9902_005.tar'

        :param filename: filename of the bulk archive file
        :return: str, URI of the bulk archive file

        :raises ValueError: if the filename does not follow the bulk archive file naming scheme
        """

        base_uri = 's3://arxiv/src/'
        if not Patterns.is_bulk_archive_filename(filename):
            raise ValueError(f"Filename {filename} does not match arXiv bulk archive naming scheme")

        base_filename = FileName.get_file_basename(filename)
        return f"{base_uri}{base_filename}"

    @staticmethod
    def parse_old_style_submission_filename(filename: str) -> tuple[str, str, str, str] | None:
        """
        Parse an older-style arXiv submission filename (pre-2008) and extract its components.

        Older arXiv submission filenames follow the pattern:
            {category}{yy}{mm}{number}.{ext}
        where:
            - category: subject area (e.g., 'cond-mat')
            - yy: last two digits of the year (e.g., '96' for 1996)
            - mm: two-digit month (e.g., '02' for February)
            - number: submission number within the month (e.g., '101')
            - ext: file extension, either '.gz' or '.pdf'

        Example:
            'cond-mat9602101.gz' → ('cond-mat', '96', '02', '101')
            (This corresponds to cond-mat/9602101 on arXiv, submitted in February 1996.)

        :param filename: str, the submission filename (may include a path)
        :return: tuple (category, yy, mm, number) if the filename matches the pattern, else None
        """

        basename = FileName.get_file_basename(filename)
        basename_no_ext, ext = os.path.splitext(basename)
        result = None
        if ext in {'.gz', '.pdf'}:
            match = re.match(r'^([a-z\-]+)(\d{2})(\d{2})(\d{3})$', basename_no_ext)
            if match:
                category, yy, mm, number = match.groups()
                result = (category, yy, mm, number)
        return result

    @staticmethod
    def parse_current_style_submission_filename(filename: str) -> tuple[str, str, str] | None:
        """
        Parse a newer-style arXiv submission filename and extract its components.

        Newer arXiv submission filenames follow the pattern:
            {yymm}.{number}.{ext}
        where:
            - yy: last two digits of the year (e.g., '12' for 2012)
            - mm: two-digit month (e.g., '02' for February)
            - number: submission number within the month (e.g., '3054')
            - ext: file extension, either '.gz' or '.pdf'

        Example:
            '1202.3054.gz' → ('12', '02', '3054')
            (This corresponds to arXiv/1202.3054, submitted in February 2012.)

        :param filename: str, the submission filename (may include a path)
        :return: tuple (yy, mm, number) if the filename matches the pattern, else None
        """
        basename = FileName.get_file_basename(filename)
        basename_no_ext, ext = os.path.splitext(basename)
        result = None
        if ext in {'.gz', '.pdf'}:
            match = re.match(r'^(\d{2})(\d{2})\.(\d{4,5})$', basename_no_ext)
            if match:
                yy, mm, number = match.groups()
                result = (yy, mm, number)
        return result

    @staticmethod
    def is_submission_filename(filename: str) -> bool:
        """
        Determine if the provided file path corresponds to the arXiv submission filename scheme.

        The filename must match either the old or current style submission pattern,
        and the extracted month must be between '01' and '12' (inclusive).

        :param filename: str, the submission filename (may include a path)
        :return: bool, True if the filename matches a submission pattern and has a valid month, else False
        """
        result = False
        old = Patterns.parse_old_style_submission_filename(filename)
        if old is not None:
            _, _, mm, _ = old
            result = mm.isdigit() and 1 <= int(mm) <= 12
        else:
            current = Patterns.parse_current_style_submission_filename(filename)
            if current is not None:
                _, mm, _ = current
                result = mm.isdigit() and 1 <= int(mm) <= 12
        return result

    @staticmethod
    def generate_url_for_submission_filename(filename: str) -> str:
        """
        Generate the URL for the given arXiv submission filename.

        Submission filenames have one of the two patterns:
            1. Subject and number (older classification scheme, pre-2008):
               e.g., cond-mat9602101.gz → https://arxiv.org/abs/cond-mat/9602101
            2. Number only (newest classification scheme):
               e.g., 1202.3054.gz → https://arxiv.org/abs/1202.3054

        The method uses the appropriate parsing method to extract the relevant components and constructs
        the canonical arXiv URL for the submission.

        :param filename: str, file name (may include a path)
        :return: str, URL pointer to arXiv for the specified arXiv submission

        :raises ValueError: if the filename does not match a valid arXiv submission pattern.
        """
        base_url = 'https://arxiv.org/abs/'

        url = None
        old = Patterns.parse_old_style_submission_filename(filename)
        if old is not None:
            category, yy, mm, number = old
            url = f"{base_url}{category}/{yy}{mm}{number}"
        else:
            current = Patterns.parse_current_style_submission_filename(filename)
            if current is not None:
                yy, mm, number = current
                url = f"{base_url}{yy}{mm}.{number}"
        if url is None:
            raise ValueError(f"Invalid arXiv submission filename: {filename}")
        
        return url

    @staticmethod
    def check_bulk_archive(file_path: str) -> list[str]:
        """
        Validate an arXiv bulk archive file and return a list of error messages describing any issues found.

        This method performs a series of checks to ensure the file is a valid arXiv bulk archive:
          1. Checks that the filename matches the expected arXiv bulk archive naming pattern.
          2. Checks that the file exists at the specified path.
          3. Checks that the file extension and format are both recognized as a tar archive.
          4. Checks that the archive can be safely extracted (e.g., no filename collisions, traversal, etc.).
          5. Checks that all entries inside the archive match the expected arXiv submission filename pattern.

        The method stops further checks if a critical error is found at any stage (e.g., invalid filename or file not found).

        :param file_path: str, path to the bulk archive file to validate.
        :returns: list[str], a list of error messages.
            If the list is empty, the bulk archive file is considered valid and extraction is possible.
        """

        error_list = []

        # Check filename pattern
        if not Patterns.is_bulk_archive_filename(file_path):
            error_list.append(f'Filename {file_path} does not match bulk archive pattern')

        # Check file existence only if pattern is valid
        if not error_list:
            if not FileSystem.is_file(file_path):
                error_list.append(f'File {file_path} not found')

        # Check file type only if previous checks passed
        if not error_list:
            if FileType.FILE_TYPE_ARCHIVE_TAR not in FileHandler.get_file_type_from_extension(file_path):
                error_list.append('File extension is not tar')
            elif FileType.FILE_TYPE_ARCHIVE_TAR != FileHandler.get_file_type_from_format(file_path):
                error_list.append('File format is not tar')

        # check that the archive could be in principle extracted
        if not error_list:
            default_extract_path = '/'
            archive_errors = ArchiveHandler.check_extract_possible(file_path, default_extract_path)
            error_list.extend(archive_errors)

        if not error_list:
            archive_contents = ArchiveHandler.list_contents(file_path)
            invalid_entries = [entry for entry in archive_contents if not Patterns.is_submission_filename(entry)]
            if invalid_entries:
                error_list.append(f"Archive entries do not match submission filename pattern: {', '.join(invalid_entries)}")

        return error_list

    @staticmethod
    def is_bulk_archive_valid(file_path: str) -> bool:
        """
        Check if the given file is a valid arXiv bulk archive.
        See check_bulk_archive() for the list of checks.

        :param file_path: str, path to the bulk archive file to validate.
        :return: bool, True if the file is a valid bulk archive, False otherwise.
        """

        return len(Patterns.check_bulk_archive(file_path)) == 0

    @staticmethod
    def check_submission(file_path: str) -> list[str]:
        """
        Validate an arXiv submission file and return a list of error messages describing any issues found.

        This method performs a series of checks to ensure the file is a valid arXiv submission:
          1. Checks that the filename matches the expected arXiv submission naming pattern.
          2. Checks that the file exists at the specified path.
          3. Checks that the file extension and format are among the allowed types (GZ, TGZ, or PDF).
          4. Checks that the file format matches the file extension.
          5. If the file is an archive (GZ or TGZ), checks that it can be safely extracted.

        The method stops further checks if a critical error is found at any stage (e.g., invalid filename or file not found).

        :param file_path: str, path to the submission file to validate.
        :return: list[str], a list of error messages. If the list is empty, the file is considered valid.
        """

        allowed_file_types = [FileType.FILE_TYPE_ARCHIVE_GZ, FileType.FILE_TYPE_ARCHIVE_TGZ, FileType.FILE_TYPE_PDF]
        allowed_archive_file_types = [FileType.FILE_TYPE_ARCHIVE_GZ, FileType.FILE_TYPE_ARCHIVE_TGZ]

        error_list = []

        # Check filename pattern
        if not Patterns.is_submission_filename(file_path):
            error_list.append(f'Filename {file_path} does not match submission pattern')

        # Check file existence only if pattern is valid
        if not error_list:
            if not FileSystem.is_file(file_path):
                error_list.append(f'File {file_path} not found')

        # Check file type only if previous checks passed
        if not error_list:
            file_types_by_extension = FileHandler.get_file_type_from_extension(file_path)
            file_type_by_format = FileHandler.get_file_type_from_format(file_path)

            if not any(file_type in allowed_file_types for file_type in file_types_by_extension):
                error_list.append('File extension type is not allowed')
            elif file_type_by_format not in allowed_file_types:
                error_list.append(f'File type {file_type_by_format.value} not allowed')
            elif file_type_by_format not in file_types_by_extension:
                error_list.append('File format does not match file extension')

            # check that the archive could be in principle extracted
            if not error_list and (file_type_by_format in allowed_archive_file_types):
                default_extract_path = '/'
                archive_errors = ArchiveHandler.check_extract_possible(file_path, default_extract_path)
                error_list.extend(archive_errors)

        return error_list

    @staticmethod
    def is_submission_valid(file_path: str) -> bool:
        """
        Check if the given file is a valid arXiv submission.
        See check_submission() for the list of checks.

        :param file_path: str, path to the submission file to validate.
        :return: bool, True if the file is a validsubmission, False otherwise.
        """

        return len(Patterns.check_submission(file_path)) == 0
