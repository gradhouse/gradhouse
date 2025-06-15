# File: submission_type.py
# Description: Submission type categories.
#
# Copyright (c) 2025 Jason Stuber
# Licensed under the MIT License. See the LICENSE file for more details.


from enum import Enum


class SubmissionType(Enum):
    """
    Enumeration for submission type categories.

    This enum is used to categorize submissions based on their extension or format.
    """

    SUBMISSION_TYPE_UNKNOWN = 'UNKNOWN'

    SUBMISSION_TYPE_PDF = 'PDF'
    SUBMISSION_TYPE_POSTSCRIPT = 'POSTSCRIPT'
    SUBMISSION_TYPE_TEX = 'TEX'
