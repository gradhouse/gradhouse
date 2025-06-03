# File: test_s3_client.py
# Description: Unit tests for the S3Client class.
#
# Copyright (c) 2025 Jason Stuber
# Licensed under the MIT License. See the LICENSE file for more details.

import subprocess
import pytest
from gradhouse.aws.s3_client import S3Client, S3ClientError


def test_copy_object_from_s3_success(monkeypatch, tmp_path):
    """
    Test that copy_object_from_s3 calls the AWS CLI with correct arguments and succeeds.
    """
    called = {}
    def fake_run(cmd, check, timeout):
        called['cmd'] = cmd
        called['check'] = check
        called['timeout'] = timeout
        return 0
    monkeypatch.setattr("subprocess.run", fake_run)
    dest_file = tmp_path / "file.txt"
    dest_dir = str(tmp_path)
    S3Client.copy_object_from_s3("s3://bucket/key", str(dest_file))
    assert called['cmd'][0:4] == ['aws', 's3', 'cp', '--request-payer']

def test_copy_object_from_s3_invalid_source():
    """
    Test that copy_object_from_s3 raises ValueError for invalid source_uri.
    """
    with pytest.raises(ValueError):
        S3Client.copy_object_from_s3("not-an-s3-uri", "/tmp/file.txt")

def test_copy_object_from_s3_invalid_dest():
    """
    Test that copy_object_from_s3 raises ValueError for invalid destination_directory.
    """
    with pytest.raises(ValueError):
        S3Client.copy_object_from_s3("s3://bucket/key", None)

def test_copy_object_from_s3_missing_directory(monkeypatch, tmp_path):
    """
    Test that copy_object_from_s3 raises FileNotFoundError if the destination directory does not exist.
    """
    monkeypatch.setattr("gradhouse.file.file_system.FileSystem.is_directory", lambda d: False)
    dest_file = tmp_path / "not_a_dir" / "file.txt"
    with pytest.raises(FileNotFoundError):
        S3Client.copy_object_from_s3("s3://bucket/key", str(dest_file))

def test_copy_object_from_s3_timeout(monkeypatch, tmp_path):
    """
    Test that copy_object_from_s3 raises S3ClientError on subprocess.TimeoutExpired.
    """
    def fake_run(*a, **k):
        raise subprocess.TimeoutExpired(cmd="aws s3 cp", timeout=300)
    monkeypatch.setattr("subprocess.run", fake_run)
    dest_file = tmp_path / "file.txt"
    monkeypatch.setattr("gradhouse.file.file_system.FileSystem.is_directory", lambda d: True)
    with pytest.raises(S3ClientError):
        S3Client.copy_object_from_s3("s3://bucket/key", str(dest_file))

def test_copy_object_from_s3_subprocess_error(monkeypatch, tmp_path):
    """
    Test that copy_object_from_s3 raises S3ClientError on subprocess.CalledProcessError.
    """
    def fake_run(*a, **k):
        raise subprocess.CalledProcessError(returncode=1, cmd="aws s3 cp")
    monkeypatch.setattr("subprocess.run", fake_run)
    dest_file = tmp_path / "file.txt"
    monkeypatch.setattr("gradhouse.file.file_system.FileSystem.is_directory", lambda d: True)
    with pytest.raises(S3ClientError):
        S3Client.copy_object_from_s3("s3://bucket/key", str(dest_file))

def test_list_directory_from_s3_success(monkeypatch):
    """
    Test that list_directory_from_s3 parses AWS CLI output correctly.
    """
    output = "2023-01-01 12:00:00      1234 file1.txt\n2023-01-01 12:01:00      5678 file2.txt\n"
    class Result:
        stdout = output
    monkeypatch.setattr("subprocess.run", lambda *a, **k: Result())
    result = S3Client.list_directory_from_s3("s3://bucket/")
    assert result == [
        {'date': '2023-01-01', 'time': '12:00:00', 'size': '1234', 'name': 'file1.txt'},
        {'date': '2023-01-01', 'time': '12:01:00', 'size': '5678', 'name': 'file2.txt'},
    ]

def test_list_directory_from_s3_invalid_uri():
    """
    Test that list_directory_from_s3 raises ValueError for invalid S3 URI.
    """
    with pytest.raises(ValueError):
        S3Client.list_directory_from_s3("not-an-s3-uri")

def test_list_directory_from_s3_timeout(monkeypatch):
    """
    Test that list_directory_from_s3 raises S3ClientError on subprocess.TimeoutExpired.
    """
    def fake_run(*a, **k):
        raise subprocess.TimeoutExpired(cmd="aws s3 ls", timeout=60)
    monkeypatch.setattr("subprocess.run", fake_run)
    with pytest.raises(S3ClientError):
        S3Client.list_directory_from_s3("s3://bucket/")

def test_list_directory_from_s3_subprocess_error(monkeypatch):
    """
    Test that list_directory_from_s3 raises S3ClientError on subprocess.CalledProcessError.
    """
    def fake_run(*a, **k):
        raise subprocess.CalledProcessError(returncode=1, cmd="aws s3 ls")
    monkeypatch.setattr("subprocess.run", fake_run)
    with pytest.raises(S3ClientError):
        S3Client.list_directory_from_s3("s3://bucket/")

def test_parse_aws_ls_output_files_and_dirs():
    """
    Test that _parse_aws_ls_output correctly parses files and directories.
    """
    output = (
        "2023-01-01 12:00:00      1234 file1.txt\n"
        "2023-01-01 12:01:00      5678 file2.txt\n"
        "2023-01-01 12:02:00 dir1/\n"
    )
    result = S3Client._parse_aws_ls_output(output)
    assert result == [
        {'date': '2023-01-01', 'time': '12:00:00', 'size': '1234', 'name': 'file1.txt'},
        {'date': '2023-01-01', 'time': '12:01:00', 'size': '5678', 'name': 'file2.txt'},
        {'date': '2023-01-01', 'time': '12:02:00', 'size': None, 'name': 'dir1/'},
    ]

def test_parse_aws_ls_output_invalid_line():
    """
    Test that _parse_aws_ls_output raises ValueError on unexpected line format.
    """
    output = "2023-01-01 file1.txt"  # Only 2 parts, which is invalid
    with pytest.raises(ValueError):
        S3Client._parse_aws_ls_output(output)

def test_parse_aws_ls_output_ignores_empty_lines():
    """
    Test that _parse_aws_ls_output ignores empty lines in the output.
    """
    output = "\n\n"
    assert S3Client._parse_aws_ls_output(output) == []

def test_parse_aws_ls_output_invalid_line_five_parts():
    """
    Test that _parse_aws_ls_output raises ValueError on a line with five parts.
    """
    output = "2023-01-01 12:00:00 1234 file1.txt extra"
    with pytest.raises(ValueError):
        S3Client._parse_aws_ls_output(output)

def test_parse_aws_ls_output_whitespace_line():
    """
    Test that _parse_aws_ls_output ignores lines with only whitespace.
    """
    output = "   \n"
    assert S3Client._parse_aws_ls_output(output) == []

def test_parse_aws_ls_output_middle_empty_line():
    """
    Test that _parse_aws_ls_output hits the else branch for an empty line in the middle.
    """
    output = "2023-01-01 12:00:00 1234 file1.txt\n\n2023-01-01 12:01:00 5678 file2.txt"
    assert S3Client._parse_aws_ls_output(output) == [
        {'date': '2023-01-01', 'time': '12:00:00', 'size': '1234', 'name': 'file1.txt'},
        {'date': '2023-01-01', 'time': '12:01:00', 'size': '5678', 'name': 'file2.txt'},
    ]