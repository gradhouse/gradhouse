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

        basename = os.path.basename(filename)
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

        base_filename = os.path.basename(filename)
        return f"{base_uri}{base_filename}"

    @staticmethod
    def parse_old_style_submission_filename(filename: str) -> tuple[str, str, str, str] | None:
        """
        Parse an older-style arXiv submission filename and extract its components.

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

        basename = os.path.basename(filename)
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
        basename = os.path.basename(filename)
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
            1. Subject and number (older classification scheme):
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
