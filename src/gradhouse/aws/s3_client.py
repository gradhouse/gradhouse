# File: s3_client.py
# Description: Static utility methods for interacting with AWS S3 using the AWS CLI.
# 
# Copyright (c) 2025 Jason Stuber
# Licensed under the MIT License. See the LICENSE file for more details.

import os
import subprocess
from typing import List, Dict, Optional

from gradhouse.file.file_system import FileSystem


class S3ClientError(Exception):
    """
    Exception raised for errors encountered during AWS S3 operations
    performed by the S3Client class.

    This exception is used to indicate operational failures such as
    timeouts, command errors, or invalid responses from the AWS CLI.
    """
    pass

class S3Client:
    """
    Static utility class for interacting with AWS (Amazon Web Services) S3 using the AWS CLI.

    This class provides static methods to perform common S3 operations such as copying objects
    from an S3 bucket to a local destination and listing the contents of an S3 directory. All
    operations are performed using the AWS CLI with requester-pays enabled, making it suitable
    for accessing public datasets that require the requester to pay for data transfer.

    Key Features:
    - Validates S3 URIs and local file paths before performing operations.
    - Handles timeouts and errors gracefully, raising S3ClientError for operational failures.
    - Parses AWS CLI output into structured Python data for easy downstream processing.
    - Does not require boto3 or AWS SDK dependencies; relies solely on the AWS CLI.

    Example usage:
        S3Client.copy_object_from_s3('s3://my-bucket/myfile.txt', '/tmp/myfile.txt')
        files = S3Client.list_directory_from_s3('s3://my-bucket/data/')

    Note:
    - The AWS CLI must be installed and configured on the system where this code runs.
      See: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html
    - The user must have appropriate AWS permissions for the requested operations.
    """

    @staticmethod
    def copy_object_from_s3(source_uri: str, destination_directory: str, timeout: Optional[int] = 300) -> None:
        """
        Copy an object from an AWS S3 bucket to a local destination using the AWS CLI.

        The method validates the source S3 URI and the local destination path, then performs
        the copy operation using the AWS CLI with requester-pays enabled. If the operation
        fails or times out, a S3ClientError is raised.

        :param source_uri: str,  The full S3 URI of the object to copy (e.g., 's3://bucket/key').
        :param destination_directory: str, The local file path where the object will be copied.
        :param timeout: int, optional timeout in seconds for the copy operation (default: 300).

        :raises ValueError: If the source_uri does not start with 's3://' or destination is invalid.
        :raises FileNotFoundError: If the destination directory does not exist.
        :raises S3ClientError: If the copy operation fails or times out.
        """

        if not source_uri.startswith("s3://"):
            raise ValueError("source_uri must start with 's3://'")

        if not destination_directory or not isinstance(destination_directory, str):
            raise ValueError("destination must be a valid file path")

        dest_dir = os.path.dirname(destination_directory) or "."
        if not FileSystem.is_directory(dest_dir):
            raise FileNotFoundError(f"Destination directory does not exist: {dest_dir}")

        command_list = [
            'aws', 's3', 'cp', '--request-payer', 'requester', source_uri, destination_directory
        ]

        try:
            subprocess.run(command_list, check=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            raise S3ClientError(f"Timeout while copying {source_uri}")
        except subprocess.CalledProcessError as e:
            raise S3ClientError(f"Failed to copy {source_uri} to {destination_directory}: {e}")
        
    @staticmethod
    def list_directory_from_s3(directory_uri: str, timeout: Optional[int] = 60) -> List[Dict[str, str]]:
        """
        List the contents of a directory in an AWS S3 bucket using the AWS CLI.

        The method validates the S3 directory URI, then performs the list operation using the AWS CLI
        with requester-pays enabled. The output is parsed into a list of dictionaries, each representing
        a file or subdirectory entry.

        :param directory_uri: str, The full S3 URI of the directory to list (e.g., 's3://bucket/prefix/').
        :param timeout: int, Optional timeout in seconds for the list operation (default: 60).

        :return: list, List of dictionaries, each containing keys: 'date', 'time', 'size', and 'name'.

        :raises ValueError: If the directory_uri does not start with 's3://'.
        :raises S3ClientError: If the list operation fails or times out.
        """
        if not directory_uri.startswith("s3://"):
            raise ValueError("directory_uri must start with 's3://'")

        command_list = [
            'aws', 's3', 'ls', '--request-payer', 'requester', directory_uri
        ]
        try:
            result = subprocess.run(command_list, capture_output=True, text=True, check=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            raise S3ClientError(f"Timeout while listing {directory_uri}")
        except subprocess.CalledProcessError as e:
            raise S3ClientError(f"Failed to list directory {directory_uri}: {e}")

        return S3Client._parse_aws_ls_output(result.stdout)

    @staticmethod
    def _parse_aws_ls_output(output: str) -> List[Dict[str, str]]:
        """
        Parse the output of the AWS CLI 'aws s3 ls' command into a list of dictionaries.

        Each line of the output is split into its components. Lines with four parts are assumed
        to represent files (date, time, size, name), while lines with three parts are assumed to
        represent directories (date, time, name). The parsed entries are returned as a list of
        dictionaries with keys: 'date', 'time', 'size', and 'name'. For directories, 'size' is None.

        :param output: str, the raw string output from the AWS CLI 'aws s3 ls' command.

        :return: List of dictionaries, each containing keys: 'date', 'time', 'size', and 'name'.
                 For directories, 'size' will be None.

        :raises ValueError: If a line in the output does not match the expected format.
        """
        
        entries = []
        for line in output.strip().splitlines():
            parts = line.split()
            if len(parts) == 4:
                date, time, size, name = parts
                entries.append({'date': date, 'time': time, 'size': size, 'name': name})
            elif len(parts) == 3:
                date, time, name = parts
                entries.append({'date': date, 'time': time, 'size': None, 'name': name})
            elif len(parts) > 0:  # raise on malformed lines
                raise ValueError(f"Unexpected line format in aws s3 ls output: '{line}'")
            else:
                # Ignore empty lines
                pass

        return entries
