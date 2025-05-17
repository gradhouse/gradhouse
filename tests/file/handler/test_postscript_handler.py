# File: test_postscript_handler.py
# Description: Unit tests for the PostscriptHandler class.
#
# Copyright (c) 2025 Jason Stuber
# Licensed under the MIT License. See the LICENSE file for more details.

import os
import pytest

from gradhouse.file.handler.postscript_handler import PostscriptHandler
from gradhouse.file.file_type import FileType


# test data directory
TEST_DIRECTORY = os.path.dirname(os.path.dirname(__file__))
TEST_DATA_DIRECTORY = os.path.join(TEST_DIRECTORY, 'sample_files')


@pytest.mark.parametrize("file_extension, expected_type", [
    ('.ps', [FileType.FILE_TYPE_POSTSCRIPT_PS]),
    ('.eps', [FileType.FILE_TYPE_POSTSCRIPT_EPS]),
    ('.epsf', [FileType.FILE_TYPE_POSTSCRIPT_EPSF]),
    ('.epsi', [FileType.FILE_TYPE_POSTSCRIPT_EPSI]),
    ('.epsijk', [FileType.FILE_TYPE_UNKNOWN]),
    ('', [FileType.FILE_TYPE_UNKNOWN]),
])
def test_get_file_type_from_extension(file_extension, expected_type):
    """
    Test the get_file_type_from_extension function
    """
    file_type = PostscriptHandler.get_file_type_from_extension(file_extension)
    assert file_type == expected_type

@pytest.mark.parametrize("filename, expected_is_ps_file", [
    ('pdf/pdf_file.pdf', False),            # not a ps file
    ('ps/ps_file.ps', True),                # ps file with correct formatting
    ('ps/eps_file.eps', True),              # eps file
    ('ps/ps_file_wrong_header.ps', False),  # ps file with the wrong header
])
def test_is_postscript_format(filename, expected_is_ps_file):
    """
    Test the is_postscript method when a file is present
    """
    full_path = os.path.join(TEST_DATA_DIRECTORY, filename)
    is_ps_file = PostscriptHandler.is_postscript_format(full_path)
    assert is_ps_file == expected_is_ps_file

def test_is_postscript_raise_file_not_found():
    """
    Test the is_postscript method when the file is not found or the path directs to a non-file
    """
    # test case: directory, is_postscript is only for files
    file_path = TEST_DATA_DIRECTORY
    with pytest.raises(FileNotFoundError):
        PostscriptHandler.is_postscript_format(file_path)

    # test case: file not found
    file_path = 'this_is_not_a_file'
    with pytest.raises(FileNotFoundError):
        PostscriptHandler.is_postscript_format(file_path)

@pytest.mark.parametrize("filename, expected_file_type", [
    ('pdf/pdf_file.pdf', FileType.FILE_TYPE_UNKNOWN),           # not a ps file
    ('ps/ps_file.ps', FileType.FILE_TYPE_POSTSCRIPT_PS),        # ps file with correct formatting
    ('ps/eps_file.eps', FileType.FILE_TYPE_POSTSCRIPT_PS),      # eps file
    ('ps/ps_file_wrong_header.ps', FileType.FILE_TYPE_UNKNOWN), # ps file with the wrong header
])
def test_get_file_type_from_format(filename, expected_file_type):
    """
    Test the get_file_type_from_format method when the file is present.
    """
    full_path = os.path.join(TEST_DATA_DIRECTORY, filename)
    file_type = PostscriptHandler.get_file_type_from_format(full_path)
    assert file_type == expected_file_type

def test_get_file_extension_map():
    """
    Test that get_file_extension_map returns the correct file extension map.
    """

    expected_map = {
        '.ps' : [FileType.FILE_TYPE_POSTSCRIPT_PS],
        '.eps': [FileType.FILE_TYPE_POSTSCRIPT_EPS],
        '.epsf': [FileType.FILE_TYPE_POSTSCRIPT_EPSF],
        '.epsi': [FileType.FILE_TYPE_POSTSCRIPT_EPSI]
    }
    result = PostscriptHandler.get_file_extension_map()

    assert isinstance(result, dict), "The result should be a dictionary."
    assert result == expected_map, "The returned file extension map is incorrect."