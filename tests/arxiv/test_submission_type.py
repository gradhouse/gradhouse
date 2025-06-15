# File: test_submission_type.py
# Description: Unit tests for the SubmissionType class.
#
# Copyright (c) 2025 Jason Stuber
# Licensed under the MIT License. See the LICENSE file for more details.

from gradhouse.arxiv.submission_type import SubmissionType


def test_enum_members_exist():
    """
    Test that the SubmissionType members are present
    """
    assert hasattr(SubmissionType, 'SUBMISSION_TYPE_UNKNOWN')

    assert hasattr(SubmissionType, 'SUBMISSION_TYPE_POSTSCRIPT')
    assert hasattr(SubmissionType, 'SUBMISSION_TYPE_TEX')

def test_enum_values():
    """
    Test that the SubmissionType enum values match expected values
    """
    assert SubmissionType.SUBMISSION_TYPE_UNKNOWN.value == 'UNKNOWN'

    assert SubmissionType.SUBMISSION_TYPE_POSTSCRIPT.value == 'POSTSCRIPT'
    assert SubmissionType.SUBMISSION_TYPE_TEX.value == 'TEX'

def test_enum_no_extra_members():
    """
    Test that no new members have been added to the SubmissionType enum.
    """

    expected_members = {
        'SUBMISSION_TYPE_UNKNOWN',
         'SUBMISSION_TYPE_POSTSCRIPT',
         'SUBMISSION_TYPE_TEX'}

    actual_members = set(SubmissionType.__members__.keys())
    assert actual_members == expected_members, f"Unexpected members found: {actual_members - expected_members}"
