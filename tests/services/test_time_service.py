# File: test_time_service.py
# Description: Unit tests for the TimeService classes.
#
# Copyright (c) 2025 Jason Stuber
# Licensed under the MIT License. See the LICENSE file for more details.

from gradhouse.services.time_service import TimeService

def test_is_iso_timestamp_newer_true():
    """
    Test that is_iso_timestamp_newer returns True when the first timestamp is newer.
    """
    assert TimeService.is_iso_timestamp_newer('2022-01-01T12:00:00+00:00', '2021-12-31T23:59:59+00:00') is True

def test_is_iso_timestamp_newer_false():
    """
    Test that is_iso_timestamp_newer returns False when the first timestamp is older.
    """
    assert TimeService.is_iso_timestamp_newer('2020-01-01T00:00:00+00:00', '2021-01-01T00:00:00+00:00') is False

def test_is_iso_timestamp_newer_equal():
    """
    Test that is_iso_timestamp_newer returns False when the timestamps are equal.
    """
    ts = '2022-05-05T15:30:00+00:00'
    assert TimeService.is_iso_timestamp_newer(ts, ts) is False

def test_is_iso_timestamp_newer_with_timezone_difference():
    """
    Test that is_iso_timestamp_newer correctly compares timestamps with different timezone offsets.
    """
    # These represent the same moment in time
    ts1 = '2022-01-01T12:00:00+00:00'
    ts2 = '2022-01-01T13:00:00+01:00'
    assert TimeService.is_iso_timestamp_newer(ts1, ts2) is False
    assert TimeService.is_iso_timestamp_newer(ts2, ts1) is False
