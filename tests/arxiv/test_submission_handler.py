# File: test_submission_handler.py
# Description: Unit tests for the SubmissionHandler class.
#
# Copyright (c) 2025 Jason Stuber
# Licensed under the MIT License. See the LICENSE file for more details.

import pytest
from gradhouse.arxiv.submission_handler import SubmissionHandler
from gradhouse.arxiv.submission_type import SubmissionType
from gradhouse.file.file_handler import FileHandler
from gradhouse.file.file_type import FileType


@pytest.mark.parametrize(
    "file_list, mock_types, expected_type",
    [
        # Only PostScript file
        (
            ["paper.ps"],
            {"paper.ps": [FileType.FILE_TYPE_POSTSCRIPT_PS]},
            SubmissionType.SUBMISSION_TYPE_POSTSCRIPT,
        ),
        # Only TeX main file
        (
            ["main.tex"],
            {"main.tex": [FileType.FILE_TYPE_TEX_TEX]},
            SubmissionType.SUBMISSION_TYPE_TEX,
        ),
        # TeX main file and supporting files
        (
            ["main.tex", "fig1.png", "refs.bib"],
            {
                "main.tex": [FileType.FILE_TYPE_TEX_TEX],
                "fig1.png": [FileType.FILE_TYPE_IMAGE_PNG],
                "refs.bib": [FileType.FILE_TYPE_TEX_BIB],
            },
            SubmissionType.SUBMISSION_TYPE_TEX,
        ),
        # TeX file and unknown file
        (
            ["main.tex", "malware.exe"],
            {
                "main.tex": [FileType.FILE_TYPE_TEX_TEX],
                "malware.exe": [],
            },
            SubmissionType.SUBMISSION_TYPE_UNKNOWN,
        ),
        # Only unknown file
        (
            ["random.xyz"],
            {"random.xyz": []},
            SubmissionType.SUBMISSION_TYPE_UNKNOWN,
        ),
        # TeX file and non-supporting known file
        (
            ["main.tex", "readme.md"],
            {
                "main.tex": [FileType.FILE_TYPE_TEX_TEX],
                "readme.md": [FileType.FILE_TYPE_UNKNOWN],
            },
            SubmissionType.SUBMISSION_TYPE_UNKNOWN,
        ),
    ]
)
def test_get_submission_type_using_extension(monkeypatch, file_list, mock_types, expected_type):
    # Patch FileHandler.get_file_type_from_extension

    def mock_get_file_type_from_extension(filename):
        return mock_types.get(filename, [])

    monkeypatch.setattr(FileHandler, "get_file_type_from_extension", staticmethod(mock_get_file_type_from_extension))

    result = SubmissionHandler.get_submission_type_using_extension(file_list)
    assert result == expected_type
