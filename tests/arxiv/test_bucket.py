# File: test_bucket.py
# Description: Unit tests for the Bucket class.
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

import pytest
from gradhouse.arxiv.bucket import Bucket
from gradhouse.aws.s3_client import S3Client

class DummyPatterns:
    @staticmethod
    def is_bulk_archive_filename(filename):
        return filename.endswith('.tar')

class DummyFileName:
    @staticmethod
    def get_file_basename(filename):
        return filename.split('/')[-1]

@pytest.fixture(autouse=True)
def patch_dependencies(monkeypatch):
    # Patch Patterns and FileName used in Bucket
    monkeypatch.setattr("gradhouse.arxiv.bucket.Patterns", DummyPatterns)
    monkeypatch.setattr("gradhouse.arxiv.bucket.FileName", DummyFileName)

def test_fetch_manifest_calls_s3client(monkeypatch, tmp_path):
    """
    Test that fetch_manifest calls S3Client.copy_object_from_s3 with the correct source and destination.
    """
    called = {}
    def fake_copy_object_from_s3(source_uri, destination_directory, timeout=300):
        called['source_uri'] = source_uri
        called['destination_directory'] = destination_directory
    monkeypatch.setattr(S3Client, "copy_object_from_s3", fake_copy_object_from_s3)
    dest = tmp_path / "manifest.xml"
    Bucket.fetch_manifest(str(dest))
    assert called['source_uri'] == f"{Bucket.ARXIV_SOURCE_S3_URI}{Bucket.ARXIV_MANIFEST_FILENAME}"
    assert called['destination_directory'] == str(dest)

def test_fetch_bulk_archive_success(monkeypatch, tmp_path):
    """
    Test that fetch_bulk_archive calls S3Client.copy_object_from_s3 with the correct source and destination
    when the filename is valid and matches the pattern.
    """
    called = {}
    def fake_copy_object_from_s3(source_uri, destination_directory, timeout=300):
        called['source_uri'] = source_uri
        called['destination_directory'] = destination_directory
    monkeypatch.setattr(S3Client, "copy_object_from_s3", fake_copy_object_from_s3)
    dest = tmp_path / "archive.tar"
    Bucket.fetch_bulk_archive("archive.tar", str(dest))
    assert called['source_uri'] == f"{Bucket.ARXIV_SOURCE_S3_URI}archive.tar"
    assert called['destination_directory'] == str(dest)

def test_fetch_bulk_archive_not_basename():
    """
    Test that fetch_bulk_archive raises ValueError if the filename is not identical to its basename.
    """
    with pytest.raises(ValueError, match="should be identical to the basename"):
        Bucket.fetch_bulk_archive("foo/bar/archive.tar", "/tmp/archive.tar")

def test_fetch_bulk_archive_invalid_pattern():
    """
    Test that fetch_bulk_archive raises ValueError if the filename does not match the expected pattern.
    """
    with pytest.raises(ValueError, match="Invalid bulk archive filename"):
        Bucket.fetch_bulk_archive("archive.txt", "/tmp/archive.txt")
