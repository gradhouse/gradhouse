# File: test_bulk_archive.py
# Description: Unit tests for the BulkArchive class.
#
# Copyright (c) 2025 Jason Stuber
# Licensed under the MIT License. See the LICENSE file for more details.
#
# Disclaimer:
# This project is not affiliated with, endorsed by, or sponsored by arXiv or Cornell University.
# arXiv® is a registered trademark of Cornell University.
# All arXiv data and trademarks are the property of their respective owners.
# For more information, see https://arxiv.org/help/license and https://info.arxiv.org/help/bulk_data_s3.html

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
