# File: test_image_handler.py
# Description: Unit tests for the ImageHandler class.
#
# Copyright (c) 2025 Jason Stuber
# Licensed under the MIT License. See the LICENSE file for more details.

import os
import pytest

from gradhouse.file.handler.image_handler import ImageHandler
from gradhouse.file.file_type import FileType

# test data directory
TEST_DIRECTORY = os.path.dirname(os.path.dirname(__file__))
TEST_DATA_DIRECTORY = os.path.join(TEST_DIRECTORY, 'sample_files')

@pytest.mark.parametrize("file_extension, expected_type", [
    ('.bmp', [FileType.FILE_TYPE_IMAGE_BMP]),
    ('.gif', [FileType.FILE_TYPE_IMAGE_GIF]),
    ('.ico', [FileType.FILE_TYPE_IMAGE_ICO]),
    ('.jpeg', [FileType.FILE_TYPE_IMAGE_JPG]),
    ('.jpg', [FileType.FILE_TYPE_IMAGE_JPG]),
    ('.png', [FileType.FILE_TYPE_IMAGE_PNG]),
    ('.tif', [FileType.FILE_TYPE_IMAGE_TIFF]),
    ('.tiff', [FileType.FILE_TYPE_IMAGE_TIFF]),
    ('.gifx', [FileType.FILE_TYPE_UNKNOWN]),
    ('', [FileType.FILE_TYPE_UNKNOWN]),
])
def test_get_file_type_from_extension(file_extension, expected_type):
    """
    Test the get_file_type_from_extension function.
    """
    file_type = ImageHandler.get_file_type_from_extension(file_extension)
    assert file_type == expected_type

@pytest.mark.parametrize("filename, expected_file_type", [
    ('pdf/pdf_file.pdf', FileType.FILE_TYPE_UNKNOWN),                 # pdf file with correct format
    ('pdf/pdf_file_wrong_header.pdf', FileType.FILE_TYPE_UNKNOWN),    # pdf incorrect header
    ('pdf/pdf_file_bad_truncated.pdf', FileType.FILE_TYPE_UNKNOWN),   # pdf too short

    ('ps/ps_file.ps', FileType.FILE_TYPE_UNKNOWN),                    # ps file with correct format
    ('ps/eps_file.eps', FileType.FILE_TYPE_UNKNOWN),                  # eps file
    ('ps/ps_file_wrong_header.ps', FileType.FILE_TYPE_UNKNOWN),       # ps file wrong header

    ('image/bmp_example.bmp', FileType.FILE_TYPE_IMAGE_BMP),          # bmp
    ('image/gif_example.gif', FileType.FILE_TYPE_IMAGE_GIF),          # gif
    ('image/ico_example.ico', FileType.FILE_TYPE_IMAGE_ICO),          # ico
    ('image/jpg_example.jpg', FileType.FILE_TYPE_IMAGE_JPG),          # jpg
    ('image/png_example.png', FileType.FILE_TYPE_IMAGE_PNG),          # png
    ('image/tiff_example.tiff', FileType.FILE_TYPE_IMAGE_TIFF)        # tiff
])
def test_get_file_type_from_format(filename, expected_file_type):
    """
    Test the get_file_type_from_format method when the file is present.
    """
    full_path = os.path.join(TEST_DATA_DIRECTORY, filename)
    file_type = ImageHandler.get_file_type_from_format(full_path)
    assert file_type == expected_file_type

def test_get_file_type_from_format_raise_file_not_found():
    """
    Test the get_file_type_from_format method when the file is not found or the path directs to a non-file.
    """
    # Test case: directory, method is only for files
    file_path = TEST_DATA_DIRECTORY
    with pytest.raises(FileNotFoundError):
        ImageHandler.get_file_type_from_format(file_path)

    # Test case: file not found
    file_path = 'this_is_not_a_file'
    with pytest.raises(FileNotFoundError):
        ImageHandler.get_file_type_from_format(file_path)

def test_get_file_extension_map():
    """
    Test that get_file_extension_map returns the correct file extension map.
    """

    expected_map = {
        '.bmp': [FileType.FILE_TYPE_IMAGE_BMP],
        '.gif': [FileType.FILE_TYPE_IMAGE_GIF],
        '.ico': [FileType.FILE_TYPE_IMAGE_ICO],
        '.jpeg': [FileType.FILE_TYPE_IMAGE_JPG],
        '.jpg': [FileType.FILE_TYPE_IMAGE_JPG],
        '.png': [FileType.FILE_TYPE_IMAGE_PNG],
        '.tif': [FileType.FILE_TYPE_IMAGE_TIFF],
        '.tiff': [FileType.FILE_TYPE_IMAGE_TIFF],
    }

    result = ImageHandler.get_file_extension_map()

    assert isinstance(result, dict), "The result should be a dictionary."
    assert result == expected_map, "The returned file extension map is incorrect."

