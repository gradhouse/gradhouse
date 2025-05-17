# File: test_bulk_archive.py
# Description: Unit tests for the BulkArchive class.
#
# Copyright (c) 2025 Jason Stuber
# Licensed under the MIT License. See the LICENSE file for more details.

from gradhouse.arxiv.bulk_archive import BulkArchive

def test_bulk_archive_initialization():
    """
    Test that BulkArchive initializes with an empty _bulk_archive dictionary.
    """
    archive = BulkArchive()
    assert isinstance(archive._bulk_archive, dict)
    assert archive._bulk_archive == {}

def test_bulk_archive_clear():
    """
    Test that BulkArchive.clear() empties the _bulk_archive dictionary.
    """
    archive = BulkArchive()
    archive._bulk_archive['test'] = 'value'
    assert archive._bulk_archive != {}
    archive.clear()
    assert archive._bulk_archive == {}
