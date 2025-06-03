# File: patterns.py
# Description: Methods for interacting with the arXiv AWS S3 bucket
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

from gradhouse.aws.s3_client import S3Client
from gradhouse.file.file_name import FileName

from .patterns import Patterns

class Bucket:
    """
    Provides static methods for interacting with the arXiv AWS S3 bucket.

    This includes downloading the arXiv manifest and bulk archive files to a local directory
    using the AWS CLI. Requires the AWS CLI to be installed and configured with appropriate permissions.
    See: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html
    """

    ARXIV_SOURCE_S3_URI = 's3://arxiv/src/'
    ARXIV_MANIFEST_FILENAME = 'arXiv_src_manifest.xml'

    @staticmethod
    def fetch_manifest(destination_directory: str) -> None:
        """
        Copy the arXiv manifest file arXiv_src_manifest.xml from the AWS S3 arXiv source bucket to a local destination
        directory using the AWS CLI.

        :param destination_directory: str, the local file path where the object will be copied.
        """

        source_uri = f'{Bucket.ARXIV_SOURCE_S3_URI}{Bucket.ARXIV_MANIFEST_FILENAME}'
        S3Client.copy_object_from_s3(source_uri, destination_directory)

    @staticmethod
    def fetch_bulk_archive(bulk_archive_filename: str, destination_directory: str) -> None:
        """
        Copy a bulk archive file from the AWS S3 arXiv source bucket to a local destination
        directory using the AWS CLI.

        :param bulk_archive_filename: str, the bulk archive filename that will be copied.
        :param destination_directory: str, the local file path where the bulk archive file will be copied.
        
        :raises ValueError: If the bulk archive filename is not identical to its basename.
        :raises ValueError: If the bulk archive filename does not match the expected pattern.
        """

        if FileName.get_file_basename(bulk_archive_filename) != bulk_archive_filename:
            raise ValueError('Bulk archive filename should be identical to the basename')

        if not Patterns.is_bulk_archive_filename(bulk_archive_filename):
            raise ValueError(f'Invalid bulk archive filename: {bulk_archive_filename}')

        source_uri = f'{Bucket.ARXIV_SOURCE_S3_URI}{bulk_archive_filename}'
        S3Client.copy_object_from_s3(source_uri, destination_directory)
