# File: test_file_system.py
# Description: Unit tests for the FileSystem class.
#
# Copyright (c) 2025 Jason Stuber
# Licensed under the MIT License. See the LICENSE file for more details.

from datetime import datetime, timezone
import os
import pytest
from gradhouse.file.file_system import FileSystem

# test data directory
TEST_DIRECTORY = os.path.dirname(__file__)
TEST_DATA_DIRECTORY = os.path.join(TEST_DIRECTORY, 'sample_files')

def test_is_file():
    """
    Test the is_file method
    """

    # test case: path is a file
    file_path = 'txt/text_file.txt'
    relative_file = os.path.join(TEST_DATA_DIRECTORY, file_path)
    assert FileSystem.is_file(relative_file)

    # test case: path is a directory
    file_path = TEST_DATA_DIRECTORY
    assert not FileSystem.is_file(file_path)

    # test case: path not found
    file_path = 'this_is_not_a_file'
    assert not FileSystem.is_file(file_path)

def test_is_directory():
    """
    Test the is_directory method
    """

    # test case: path is a directory
    dir_path = TEST_DATA_DIRECTORY
    assert FileSystem.is_directory(dir_path)

    # test case: path is a file
    dir_path = 'txt/text_file.txt'
    relative_file = os.path.join(TEST_DATA_DIRECTORY, dir_path)
    assert not FileSystem.is_directory(relative_file)

    # test case: directory not found
    dir_path = 'this_is_not_a_file'
    assert not FileSystem.is_directory(dir_path)

def test_get_file_size():
    """
    Test the get_file_size method
    """

    # test cases: file, expected_size
    test_data = [
        ['txt/text_file.txt', 9]
    ]

    for file, expected_size in test_data:
        full_path = os.path.join(TEST_DATA_DIRECTORY, file)
        file_size = FileSystem.get_file_size(full_path)
        assert file_size == expected_size

def test_get_file_size_raise_file_not_found():
    """
    Test the get_file_size method when the file is not found or the path directs to a non-file
    """

    # test case: directory, get_size is only for files
    file_path = TEST_DATA_DIRECTORY
    with pytest.raises(FileNotFoundError):
        FileSystem.get_file_size(file_path)

    # test case: file not found
    file_path = 'this_is_not_a_file'
    with pytest.raises(FileNotFoundError):
        FileSystem.get_file_size(file_path)

def test_create_directory_success(mocker):
    """
    Test the create_directory method when the method is successful.
    """

    mock_is_object = mocker.patch('gradhouse.file.file_system.FileSystem.is_object', return_value=False)
    mock_makedirs = mocker.patch('os.makedirs')
    directory_path = '/path/to/directory'

    FileSystem.create_directory(directory_path)

    mock_is_object.assert_called_once_with(directory_path)
    mock_makedirs.assert_called_once_with(directory_path, exist_ok=False)

def test_create_directory_already_exists(mocker):
    """
    Test the create_directory method when the directory or file object already exists.
    """

    mock_is_object = mocker.patch('gradhouse.file.file_system.FileSystem.is_object', return_value=True)
    directory_path = '/path/to/directory'

    with pytest.raises(FileExistsError):
        FileSystem.create_directory(directory_path)

    mock_is_object.assert_called_once_with(directory_path)

def test_create_directory_oserror(mocker):
    """
    Test the create_directory method when the directory creation was not successful.
    """

    mock_is_object = mocker.patch('gradhouse.file.file_system.FileSystem.is_object', return_value=False)
    mock_makedirs = mocker.patch('os.makedirs', side_effect=OSError("Error creating directory"))
    directory_path = '/path/to/directory'

    with pytest.raises(OSError):
        FileSystem.create_directory(directory_path)

    mock_is_object.assert_called_once_with(directory_path)
    mock_makedirs.assert_called_once_with(directory_path, exist_ok=False)

def test_is_object():
    """
    Test the is_object method
    """

    # test case: path is an existing directory
    dir_path = TEST_DATA_DIRECTORY
    assert FileSystem.is_object(dir_path)

    # test case: path is an existing file
    dir_path = 'txt/text_file.txt'
    relative_file = os.path.join(TEST_DATA_DIRECTORY, dir_path)
    assert FileSystem.is_object(relative_file)

    # test case: object not found
    dir_path = 'this_is_not_a_file'
    assert not FileSystem.is_object(dir_path)

def test_remove_directory_success(mocker):
    """
    Test the remove_directory method when it is successful.
    """

    mock_is_directory = mocker.patch('gradhouse.file.file_system.FileSystem.is_directory', return_value=True)
    mock_rmtree = mocker.patch('shutil.rmtree')
    directory_path = '/path/to/directory'

    FileSystem.remove_directory(directory_path)

    mock_is_directory.assert_called_once_with(directory_path)
    mock_rmtree.assert_called_once_with(directory_path)

def test_remove_directory_not_a_directory(mocker):
    """
    Test the remove_directory method when it is not a directory.
    """

    mock_is_directory = mocker.patch('gradhouse.file.file_system.FileSystem.is_directory', return_value=False)
    directory_path = '/path/to/directory'

    with pytest.raises(FileNotFoundError):
        FileSystem.remove_directory(directory_path)

    mock_is_directory.assert_called_once_with(directory_path)

def test_remove_directory_oserror(mocker):
    """
    Test the remove_directory method when there is an error removing the directory.
    """

    mock_is_directory = mocker.patch('gradhouse.file.file_system.FileSystem.is_directory', return_value=True)
    mock_rmtree = mocker.patch('shutil.rmtree', side_effect=OSError("Error removing directory"))
    directory_path = '/path/to/directory'

    with pytest.raises(OSError):
        FileSystem.remove_directory(directory_path)

    mock_is_directory.assert_called_once_with(directory_path)
    mock_rmtree.assert_called_once_with(directory_path)

def test_get_file_timestamp_mocked(mocker):
    """
    Test the get_file_timestamp method. Mocking is required due to the data file creation times.
    """
    # Mock the file path
    mock_file_path = "/mock/path/to/file.txt"

    # Mock FileSystem.is_file to return True
    mock_is_file = mocker.patch("gradhouse.file.file_system.FileSystem.is_file", return_value=True)

    # Mock os.stat to simulate file metadata
    mock_stat_result = mocker.Mock()
    mock_stat_result.st_mtime = 1682000000  # Example timestamp in seconds
    mock_os_stat = mocker.patch("os.stat", return_value=mock_stat_result)

    # Expected ISO 8601 timestamp
    expected_timestamp = datetime.fromtimestamp(1682000000, timezone.utc).isoformat()

    # Call the method
    result = FileSystem.get_file_timestamp(mock_file_path)

    # Assertions
    mock_is_file.assert_called_once_with(mock_file_path)
    mock_os_stat.assert_called_once_with(mock_file_path)
    assert result == expected_timestamp

def test_get_file_timestamp_raise_file_not_found():
    """
    Test the get_file_timestamp method when the file is not found or the path directs to a non-file
    """

    # test case: directory, get_file_timestamp is only for files
    file_path = TEST_DATA_DIRECTORY
    with pytest.raises(FileNotFoundError):
        FileSystem.get_file_timestamp(file_path)

    # test case: file not found
    file_path = 'this_is_not_a_file'
    with pytest.raises(FileNotFoundError):
        FileSystem.get_file_timestamp(file_path)

def test_is_utf8_encoded():
    """
    Test the is_utf8_encoded method
    """

    # test case: file is UTF-8 encoded
    file_path = os.path.join(TEST_DATA_DIRECTORY, 'txt/text_file.txt')
    is_utf8 = FileSystem.is_utf8_encoded(file_path)
    assert is_utf8

    # test case: file is not UTF-8 encoded
    file_path = os.path.join(TEST_DATA_DIRECTORY, 'txt/non_utf8_sample.txt')
    is_utf8 = FileSystem.is_utf8_encoded(file_path)
    assert not is_utf8

def test_is_utf8_encoded_raise_file_not_found():
    """
    Test the is_utf8_encoded method when the file is not found or the path directs to a non-file
    """

    # test case: directory, get_size is only for files
    file_path = TEST_DATA_DIRECTORY
    with pytest.raises(FileNotFoundError):
        FileSystem.is_utf8_encoded(file_path)

    # test case: file not found
    file_path = 'this_is_not_a_file'
    with pytest.raises(FileNotFoundError):
        FileSystem.is_utf8_encoded(file_path)

def test_list_files():
    """
    Test the list_files method
    """

    expected_top_level_files = ['top_level_text_file.txt']
    expected_sub_files = [
        'archive/gzip_single_file.gz',
        'archive/gzip_with_extra_field.gz',
        'archive/tar_archive_file.tar',
        'archive/tgz_archive_file.tgz',
        'archive/zip_archive_file.zip',
        'image/bmp_example.bmp',
        'image/gif_example.gif',
        'image/ico_example.ico',
        'image/jpg_example.jpg',
        'image/png_example.png',
        'image/svg_example.svg',
        'image/tiff_example.tiff',
        'pdf/pdf_file.pdf',
        'pdf/pdf_file_bad_truncated.pdf',
        'pdf/pdf_file_wrong_header.pdf',
        'ps/eps_file.eps',
        'ps/ps_file.ps',
        'ps/ps_file_wrong_header.ps',
        'tex/latex2e_example_non_utf8.tex',
        'tex/latex2e_example.tex',
        'tex/latex209_example.tex',
        'txt/non_utf8_sample.txt',
        'txt/text_file.txt',]

    expected_with_sub_files = expected_top_level_files + expected_sub_files

    dir_path = TEST_DATA_DIRECTORY

    # method has default subdirectory search arguments
    expected_filenames = expected_top_level_files
    filename_list = FileSystem.list_files(dir_path)
    filtered_filename_list = [fn for fn in filename_list if '__pycache__' not in fn and '.DS_Store' not in fn]
    assert set(expected_filenames) == set(filtered_filename_list)

    # method has subdirectory search False
    expected_filenames = expected_top_level_files
    filename_list = FileSystem.list_files(dir_path, include_subdirectories=False)
    filtered_filename_list = [fn for fn in filename_list if '__pycache__' not in fn and '.DS_Store' not in fn]
    assert set(expected_filenames) == set(filtered_filename_list)

    # method has subdirectory search True
    expected_filenames = expected_with_sub_files
    filename_list = FileSystem.list_files(dir_path, include_subdirectories=True)
    filtered_filename_list = [fn for fn in filename_list if '__pycache__' not in fn and '.DS_Store' not in fn]
    assert set(expected_filenames) == set(filtered_filename_list)

def test_list_files_raise_directory_not_found():
    """
    Test the list_files method when the directory is not found
    """

    # test case: path is a file, method has default subdirectory search arguments
    dir_path = 'text_file.txt'
    relative_file = os.path.join(TEST_DATA_DIRECTORY, dir_path)
    with pytest.raises(FileNotFoundError):
        FileSystem.list_files(relative_file)

    # test case: path is a file, method has subdirectory search False
    dir_path = 'text_file.txt'
    relative_file = os.path.join(TEST_DATA_DIRECTORY, dir_path)
    with pytest.raises(FileNotFoundError):
        FileSystem.list_files(relative_file, include_subdirectories=False)

    # test case: path is a file, method has subdirectory search True
    dir_path = 'txt/text_file.txt'
    relative_file = os.path.join(TEST_DATA_DIRECTORY, dir_path)
    with pytest.raises(FileNotFoundError):
        FileSystem.list_files(relative_file, include_subdirectories=True)

    # test case: directory not found, method has default subdirectory search arguments
    dir_path = 'this_is_not_a_file'
    with pytest.raises(FileNotFoundError):
        FileSystem.list_files(dir_path)

    # test case: directory not found, method has subdirectory search False
    dir_path = 'this_is_not_a_file'
    with pytest.raises(FileNotFoundError):
        FileSystem.list_files(dir_path, include_subdirectories=False)

    # test case: directory not found, method has subdirectory search True
    dir_path = 'this_is_not_a_file'
    with pytest.raises(FileNotFoundError):
        FileSystem.list_files(dir_path, include_subdirectories=True)
