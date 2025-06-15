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
from gradhouse.file.file_system import FileSystem
from gradhouse.arxiv.patterns import Patterns
from gradhouse.file.handler.archive_handler import ArchiveHandler


import pytest


@pytest.mark.parametrize(
    "file_list, mock_types, expected_type",
    [
        # Only PostScript file
        (
            ["paper.ps"],
            {"paper.ps": [FileType.FILE_TYPE_POSTSCRIPT_PS]},
            SubmissionType.SUBMISSION_TYPE_POSTSCRIPT,
        ),
        # Only PDF file
        (
                ["paper.pdf"],
                {"paper.pdf": [FileType.FILE_TYPE_PDF]},
                SubmissionType.SUBMISSION_TYPE_PDF,
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
    """
    Test SubmissionHandler.get_submission_type_using_extension with various file lists.

    This parameterized test checks that the method correctly determines the submission type
    based on the provided list of filenames and their associated file types. It uses monkeypatching
    to mock FileHandler.get_file_type_from_extension, allowing control over the file type detection.

    Scenarios tested include:
    - Only PostScript files (should return SUBMISSION_TYPE_POSTSCRIPT)
    - Only PDF files (should return SUBMISSION_TYPE_PDF)
    - Only TeX main files or TeX with supporting files (should return SUBMISSION_TYPE_TEX)
    - TeX files with unknown or unsupported files (should return SUBMISSION_TYPE_UNKNOWN)
    - Only unknown or unsupported files (should return SUBMISSION_TYPE_UNKNOWN)
    """

    def mock_get_file_type_from_extension(filename):
        return mock_types.get(filename, [])

    monkeypatch.setattr(FileHandler, "get_file_type_from_extension", staticmethod(mock_get_file_type_from_extension))

    result = SubmissionHandler.get_submission_type_using_extension(file_list)
    assert result == expected_type

@pytest.mark.parametrize(
    "file_exists, submission_errors, metadata, archive_contents, expected_type, expected_key, expected_entry",
    [
        # PDF file, no errors
        (
            True,
            [],
            {
                "hash": {"SHA256": "sha256pdf"},
                "file_type": FileType.FILE_TYPE_PDF.value,
                "other": "meta"
            },
            None,
            SubmissionType.SUBMISSION_TYPE_PDF,
            "sha256pdf",
            {
                "metadata": {
                    "hash": {"SHA256": "sha256pdf"},
                    "file_type": FileType.FILE_TYPE_PDF.value,
                    "other": "meta",
                    "submission_type_by_extension": "PDF"
                },
                "origin": {
                    "url": "http://example.com/submission",
                    "bulk_archive_hash": "bulkhash"
                }
            }
        ),
        # PDF file, with errors
        (
            True,
            ["bad format"],
            {
                "hash": {"SHA256": "sha256pdferr"},
                "file_type": FileType.FILE_TYPE_PDF.value,
                "other": "meta"
            },
            None,
            SubmissionType.SUBMISSION_TYPE_UNKNOWN,
            "sha256pdferr",
            {
                "metadata": {
                    "hash": {"SHA256": "sha256pdferr"},
                    "file_type": FileType.FILE_TYPE_PDF.value,
                    "other": "meta",
                    "submission_type_by_extension": "UNKNOWN"
                },
                "origin": {
                    "url": "http://example.com/submission",
                    "bulk_archive_hash": "bulkhash"
                },
                "diagnostics": {
                    "error_list": ["bad format"]
                }
            }
        ),
        # GZ archive, no errors, TeX contents
        (
            True,
            [],
            {
                "hash": {"SHA256": "sha256gz"},
                "file_type": FileType.FILE_TYPE_ARCHIVE_GZ.value,
                "other": "meta"
            },
            ["main.tex", "refs.bib"],
            SubmissionType.SUBMISSION_TYPE_TEX,
            "sha256gz",
            {
                "metadata": {
                    "hash": {"SHA256": "sha256gz"},
                    "file_type": FileType.FILE_TYPE_ARCHIVE_GZ.value,
                    "other": "meta",
                    "submission_type_by_extension": "TEX"
                },
                "origin": {
                    "url": "http://example.com/submission",
                    "bulk_archive_hash": "bulkhash"
                }
            }
        ),
        # GZ archive, no errors, unknown contents
        (
            True,
            [],
            {
                "hash": {"SHA256": "sha256gzunk"},
                "file_type": FileType.FILE_TYPE_ARCHIVE_GZ.value,
                "other": "meta"
            },
            ["virus.exe"],
            SubmissionType.SUBMISSION_TYPE_UNKNOWN,
            "sha256gzunk",
            {
                "metadata": {
                    "hash": {"SHA256": "sha256gzunk"},
                    "file_type": FileType.FILE_TYPE_ARCHIVE_GZ.value,
                    "other": "meta",
                    "submission_type_by_extension": "UNKNOWN"
                },
                "origin": {
                    "url": "http://example.com/submission",
                    "bulk_archive_hash": "bulkhash"
                },
                "diagnostics": {
                    "error_list": ["Unknown submission type"]
                }
            }
        ),
        # File does not exist
        (
            False,
            [],
            {},
            None,
            None,
            None,
            None
        ),
    ]
)
def test_generate_submission_entry(
    monkeypatch,
    file_exists,
    submission_errors,
    metadata,
    archive_contents,
    expected_type,
    expected_key,
    expected_entry
):
    """
    Test SubmissionHandler.generate_submission_entry for correct key/value output and error handling.

    This parameterized test covers:
    - PDF files with and without errors
    - Archive files with TeX or unknown contents
    - File not found error
    """

    # Patch FileSystem.is_file
    monkeypatch.setattr(FileSystem, "is_file", staticmethod(lambda path: file_exists))

    # Patch Patterns.check_submission
    monkeypatch.setattr(Patterns, "check_submission", staticmethod(lambda path: submission_errors))

    # Patch Patterns.generate_url_for_submission_filename
    monkeypatch.setattr(Patterns, "generate_url_for_submission_filename", staticmethod(lambda path: "http://example.com/submission"))

    # Patch FileHandler.get_metadata
    monkeypatch.setattr(FileHandler, "get_metadata", staticmethod(lambda path, hash_types=None: metadata))

    # Patch ArchiveHandler.list_contents if archive_contents is not None
    if archive_contents is not None:
        monkeypatch.setattr(ArchiveHandler, "list_contents", staticmethod(lambda path: archive_contents))

    if not file_exists:
        with pytest.raises(FileNotFoundError):
            SubmissionHandler.generate_submission_entry("dummy_path", "bulkhash")
    else:
        key, entry = SubmissionHandler.generate_submission_entry("dummy_path", "bulkhash")
        assert key == expected_key
        assert entry == expected_entry

def test_generate_submission_entry_else_submission_type_unknown(monkeypatch):
    """
    Covers the 'else' branch where the file is not an archive or PDF,
    there are no submission errors, and the file type is not allowed,
    resulting in submission_type = SUBMISSION_TYPE_UNKNOWN.
    """
    file_exists = True
    submission_errors = []
    # Use a file type that is not PDF, GZ, or TGZ
    dummy_file_type = "SOMETHING_UNSUPPORTED"
    metadata = {
        "hash": {"SHA256": "sha256dummy"},
        "file_type": dummy_file_type,
        "other": "meta"
    }
    expected_key = "sha256dummy"
    expected_entry = {
        "metadata": {
            "hash": {"SHA256": "sha256dummy"},
            "file_type": dummy_file_type,
            "other": "meta",
            "submission_type_by_extension": "UNKNOWN"
        },
        "origin": {
            "url": "http://example.com/submission",
            "bulk_archive_hash": "bulkhash"
        },
        "diagnostics": {
            "error_list": ["Unknown submission type"]
        }
    }

    monkeypatch.setattr(FileSystem, "is_file", staticmethod(lambda path: file_exists))
    # Patterns.check_submission returns no errors
    monkeypatch.setattr(Patterns, "check_submission", staticmethod(lambda path: submission_errors))
    monkeypatch.setattr(Patterns, "generate_url_for_submission_filename", staticmethod(lambda path: "http://example.com/submission"))
    monkeypatch.setattr(FileHandler, "get_metadata", staticmethod(lambda path, hash_types=None: metadata))

    key, entry = SubmissionHandler.generate_submission_entry("dummy_path", "bulkhash")
    assert key == expected_key
    assert entry == expected_entry