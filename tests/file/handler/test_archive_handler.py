# File: test_archive_handler.py
# Description: Unit tests for the ArchiveHandler class
#
# Copyright (c) 2025 Jason Stuber
# Licensed under the MIT License. See the LICENSE file for more details.

import os
import struct
import pytest

from gradhouse.file.handler.archive_handler import ArchiveHandler
from gradhouse.file.file_type import FileType

# Test data directory
TEST_DIRECTORY = os.path.dirname(os.path.dirname(__file__))
TEST_DATA_DIRECTORY = os.path.join(TEST_DIRECTORY, 'sample_files')
TEST_SCRATCH_DIRECTORY = '/'  #  only used for mocking, root path sufficient

def test_get_file_extension_map():
    """
    Test that get_file_extension_map returns the correct file extension map.
    """

    expected_map = {
        '.gz': [FileType.FILE_TYPE_ARCHIVE_GZ, FileType.FILE_TYPE_ARCHIVE_TGZ],  # .tar.gz could identify as .gz
        '.tar' : [FileType.FILE_TYPE_ARCHIVE_TAR],
        '.tgz': [FileType.FILE_TYPE_ARCHIVE_TGZ]
    }

    result = ArchiveHandler.get_file_extension_map()

    assert isinstance(result, dict), "The result should be a dictionary."
    assert result == expected_map, "The returned file extension map is incorrect."

def test_get_file_type_from_extension():
    """
    Test the get_file_type_from_extension function
    """

    # test cases: extension, expected category
    test_data = [
        ('.tar', [FileType.FILE_TYPE_ARCHIVE_TAR]),
        ('.tgz', [FileType.FILE_TYPE_ARCHIVE_TGZ]),
        ('.gz', [FileType.FILE_TYPE_ARCHIVE_GZ, FileType.FILE_TYPE_ARCHIVE_TGZ]),
        ('.targ', [FileType.FILE_TYPE_UNKNOWN]),
        ('', [FileType.FILE_TYPE_UNKNOWN])
    ]

    for file_extension, expected_type in test_data:
        file_type = ArchiveHandler.get_file_type_from_extension(file_extension)
        assert set(file_type) == set(expected_type)

@pytest.mark.parametrize("filename, expected_file_type", [
    ('archive/tar_archive_file.tar', FileType.FILE_TYPE_ARCHIVE_TAR),  # tar file
    ('archive/tgz_archive_file.tgz', FileType.FILE_TYPE_ARCHIVE_TGZ),  # tar.gz file
    ('archive/gzip_single_file.gz', FileType.FILE_TYPE_ARCHIVE_GZ),  # gzip file
    ('archive/gzip_with_extra_field.gz', FileType.FILE_TYPE_ARCHIVE_GZ),  # gzip file with extra field
    ('archive/zip_archive_file.zip', FileType.FILE_TYPE_UNKNOWN)  # zip file
])
def test_get_file_type_from_format(filename, expected_file_type):
    """
    Test the get_file_type_from_format method when the file is present.
    """
    full_path = os.path.join(TEST_DATA_DIRECTORY, filename)
    file_type = ArchiveHandler.get_file_type_from_format(full_path)
    assert expected_file_type == file_type

@pytest.mark.parametrize("filename, expected_is_archive_file", [
    ('archive/tar_archive_file.tar', True),  # tar file
    ('archive/tgz_archive_file.tgz', True),  # tar.gz file
    ('archive/gzip_single_file.gz', True),  # gzip file
    ('archive/gzip_with_extra_field.gz', True),  # gzip file with extra field
    ('archive/zip_archive_file.zip', False)  # zip file
])
def test_is_archive_format(filename, expected_is_archive_file):
    """
    Test the is_archive_format method when a file is present
    """
    full_path = os.path.join(TEST_DATA_DIRECTORY, filename)
    is_archive_file = ArchiveHandler.is_archive_format(full_path)
    assert is_archive_file == expected_is_archive_file

def test_is_archive_format_raise_file_not_found():
    """
    Test the is_archive_format method when the file is not found or the path directs to a non-file.
    """

    # test case: directory, is_archive_format is only for files
    file_path = TEST_DATA_DIRECTORY
    with pytest.raises(FileNotFoundError):
        ArchiveHandler.is_archive_format(file_path)

    # test case: file not found
    file_path = 'this_is_not_a_file'
    with pytest.raises(FileNotFoundError):
        ArchiveHandler.is_archive_format(file_path)

@pytest.mark.parametrize("filename, expected_is_tar_file", [
    ('archive/tar_archive_file.tar', True),  # tar file
    ('archive/tgz_archive_file.tgz', False),  # tar.gz file
    ('archive/gzip_single_file.gz', False),  # gzip file
    ('archive/gzip_with_extra_field.gz', False),  # gzip file with extra field
    ('archive/zip_archive_file.zip', False)  # zip file
])
def test_is_tar_format(filename, expected_is_tar_file):
    """
    Test the is_tar_format method when a file is present.
    """
    full_path = os.path.join(TEST_DATA_DIRECTORY, filename)
    is_tar_file = ArchiveHandler.is_tar_format(full_path)
    assert is_tar_file == expected_is_tar_file

def test_is_tar_format_raise_file_not_found():
    """
    Test the is_tar_format method when the file is not found or the path directs to a non-file.
    """
    # test case: directory, is_tar_format is only for files
    file_path = TEST_DATA_DIRECTORY
    with pytest.raises(FileNotFoundError):
        ArchiveHandler.is_tar_format(file_path)

    # test case: file not found
    file_path = 'this_is_not_a_file'
    with pytest.raises(FileNotFoundError):
        ArchiveHandler.is_tar_format(file_path)

@pytest.mark.parametrize("filename, expected_is_tgz_file", [
    ('archive/tar_archive_file.tar', False),  # tar file
    ('archive/tgz_archive_file.tgz', True),  # tar.gz file
    ('archive/gzip_single_file.gz', False),  # gzip file
    ('archive/gzip_with_extra_field.gz', False),  # gzip file with extra field
    ('archive/zip_archive_file.zip', False)  # zip file
])
def test_is_tgz_format(filename, expected_is_tgz_file):
    """
    Test the is_tgz_format method when a file is present.
    """
    full_path = os.path.join(TEST_DATA_DIRECTORY, filename)
    is_tgz_file = ArchiveHandler.is_tgz_format(full_path)
    assert is_tgz_file == expected_is_tgz_file

def test_is_tgz_format_raise_file_not_found():
    """
    Test the is_tgz_format method when the file is not found or the path directs to a non-file.
    """
    # test case: directory, is_tgz_format is only for files
    file_path = TEST_DATA_DIRECTORY
    with pytest.raises(FileNotFoundError):
        ArchiveHandler.is_tgz_format(file_path)

    # test case: file not found
    file_path = 'this_is_not_a_file'
    with pytest.raises(FileNotFoundError):
        ArchiveHandler.is_tgz_format(file_path)

@pytest.mark.parametrize("filename, expected_is_gzip_file", [
    ('archive/tar_archive_file.tar', False),  # tar file
    ('archive/tgz_archive_file.tgz', False),  # tar.gz file
    ('archive/gzip_single_file.gz', True),  # gzip file
    ('archive/gzip_with_extra_field.gz', True),  # gzip file with extra field
    ('archive/zip_archive_file.zip', False)  # zip file
])
def test_is_gzip_format(filename, expected_is_gzip_file):
    """
    Test the is_gzip_format method when a file is present.
    """
    full_path = os.path.join(TEST_DATA_DIRECTORY, filename)
    is_gzip_file = ArchiveHandler.is_gzip_format(full_path)
    assert is_gzip_file == expected_is_gzip_file

def test_is_gzip_format_raise_file_not_found():
    """
    Test the is_gzip_format method when the file is not found or the path directs to a non-file.
    """
    # test case: directory, is_gzip_format is only for files
    file_path = TEST_DATA_DIRECTORY
    with pytest.raises(FileNotFoundError):
        ArchiveHandler.is_gzip_format(file_path)

    # test case: file not found
    file_path = 'this_is_not_a_file'
    with pytest.raises(FileNotFoundError):
        ArchiveHandler.is_gzip_format(file_path)

@pytest.mark.parametrize("filename, expected_contents", [
    (
        'archive/tar_archive_file.tar',
        [
            'sample_archive/folder1/second_file.txt',
            'sample_archive/folder1/empty_file.txt',
            'sample_archive/folder2/another_doc.txt',
            'sample_archive/top_level_file.txt',
            'sample_archive/top_level_file.txt'
        ]
    )
])
def test_list_tar_contents(filename, expected_contents):
    """
    Test the _list_tar_contents method.
    """
    full_path = os.path.join(TEST_DATA_DIRECTORY, filename)
    file_contents = ArchiveHandler._list_tar_contents(full_path)
    file_contents_filtered = [filename for filename in file_contents if '.DS_Store' not in filename]
    assert set(file_contents_filtered) == set(expected_contents)


@pytest.mark.parametrize("file_path", [
    TEST_DATA_DIRECTORY,  # directory
    'this_is_not_a_file'  # file not found
])
def test_list_tar_contents_raise_file_not_found(file_path):
    """
    Test the _list_tar_contents when the file is not found or the path directs to a non-file.
    """
    with pytest.raises(FileNotFoundError):
        ArchiveHandler._list_tar_contents(file_path)


@pytest.mark.parametrize("filename", [
    'archive/tgz_archive_file.tgz',  # tgz file
    'archive/gzip_single_file.gz',  # gzip file
    'archive/gzip_with_extra_field.gz',  # gzip file with extra field
    'archive/zip_archive_file.zip'  # zip file
])
def test_list_tar_contents_raise_file_type_not_tar(filename):
    """
    Test the _list_tar_contents when the file type is not a tar archive.
    """
    full_path = os.path.join(TEST_DATA_DIRECTORY, filename)
    with pytest.raises(TypeError):
        ArchiveHandler._list_tar_contents(full_path)


@pytest.mark.parametrize("filename, expected_contents", [
    (
        'archive/tgz_archive_file.tgz',
        [
            'sample_archive/folder1/second_file.txt',
            'sample_archive/folder1/empty_file.txt',
            'sample_archive/folder2/another_doc.txt',
            'sample_archive/top_level_file.txt',
            'sample_archive/top_level_file.txt'
        ]
    )
])
def test_list_tgz_contents(filename, expected_contents):
    """
    Test the _list_tgz_contents.
    """
    full_path = os.path.join(TEST_DATA_DIRECTORY, filename)
    file_contents = ArchiveHandler._list_tgz_contents(full_path)
    file_contents_filtered = [filename for filename in file_contents if '.DS_Store' not in filename]
    assert set(file_contents_filtered) == set(expected_contents)


@pytest.mark.parametrize("file_path", [
    TEST_DATA_DIRECTORY,  # directory
    'this_is_not_a_file'  # file not found
])
def test_list_tgz_contents_raise_file_not_found(file_path):
    """
    Test the _list_tgz_contents when the file is not found or the path directs to a non-file.
    """
    with pytest.raises(FileNotFoundError):
        ArchiveHandler._list_tgz_contents(file_path)


@pytest.mark.parametrize("filename", [
    'archive/tar_archive_file.tar',  # tar file
    'archive/gzip_single_file.gz',  # gzip file
    'archive/gzip_with_extra_field.gz',  # gzip file with extra field
    'archive/zip_archive_file.zip'  # zip file
])
def test_list_tar_contents_raise_file_type_not_tgz(filename):
    """
    Test the _list_tgz_contents when the file type is not a tgz archive.
    """
    full_path = os.path.join(TEST_DATA_DIRECTORY, filename)
    with pytest.raises(TypeError):
        ArchiveHandler._list_tgz_contents(full_path)


@pytest.mark.parametrize("filename, expected_contents", [
    ('archive/gzip_single_file.gz', ['a_single_file.txt'])
])
def test_list_gzip_contents_gzip(filename, expected_contents):
    """
    Test the _list_gzip_contents when the file type is pure gzip.
    """
    full_path = os.path.join(TEST_DATA_DIRECTORY, filename)
    file_contents = ArchiveHandler._list_gzip_contents(full_path)
    assert set(expected_contents) == set(file_contents)


@pytest.mark.parametrize("filename, expected_contents", [
    ('archive/gzip_with_extra_field.gz', ['th_extra_field'])
])
def test_list_gzip_contents_gzip_extra_field(filename, expected_contents):
    """
    Test the _list_gzip_contents when the file type is pure gzip with an extra field.
    """
    full_path = os.path.join(TEST_DATA_DIRECTORY, filename)
    file_contents = ArchiveHandler._list_gzip_contents(full_path)
    assert set(expected_contents) == set(file_contents)


@pytest.mark.parametrize("file_path", [
    TEST_DATA_DIRECTORY,  # directory
    'this_is_not_a_file'  # file not found
])
def test_list_gzip_contents_raise_file_not_found(file_path):
    """
    Test the list_gzip_contents when the file is not found or the path directs to a non-file.
    """
    with pytest.raises(FileNotFoundError):
        ArchiveHandler._list_gzip_contents(file_path)


@pytest.mark.parametrize("filename", [
    'archive/tgz_archive_file.tgz',  # tgz file
    'archive/tar_archive_file.tar',  # tar file
    'archive/zip_archive_file.zip'  # zip file
])
def test_list_gzip_contents_raise_file_type_not_gzip(filename):
    """
    Test the _list_gzip_contents when the file type is not a gzip archive.
    """
    full_path = os.path.join(TEST_DATA_DIRECTORY, filename)
    with pytest.raises(TypeError):
        ArchiveHandler._list_gzip_contents(full_path)

def test_list_contents_tar(mocker):
    """
    Test the test_list_contents for a tar format archive.
    """
    mock_is_archive = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler.is_archive_format', return_value=True)
    mock_is_tar = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler.is_tar_format', return_value=True)
    mock_is_tgz = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler.is_tgz_format', return_value=False)
    mock_is_gzip = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler.is_gzip_format', return_value=False)
    mock_list_tar = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler._list_tar_contents', return_value=['file1.txt', 'file2.txt'])

    result = ArchiveHandler.list_contents('dummy.tar')
    assert result == ['file1.txt', 'file2.txt']
    mock_list_tar.assert_called_once_with('dummy.tar')

    mock_is_archive.assert_called_once()
    mock_is_gzip.assert_called_once()
    mock_is_tar.assert_called_once()
    mock_is_tgz.assert_not_called()

def test_list_contents_tgz(mocker):
    """
    Test the test_list_contents for a tgz format archive.
    """
    mock_is_archive = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler.is_archive_format', return_value=True)
    mock_is_tar = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler.is_tar_format', return_value=False)
    mock_is_tgz = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler.is_tgz_format', return_value=True)
    mock_is_gzip = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler.is_gzip_format', return_value=False)
    mock_list_tgz = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler._list_tgz_contents', return_value=['file1.txt', 'file2.txt'])

    result = ArchiveHandler.list_contents('dummy.tgz')
    assert result == ['file1.txt', 'file2.txt']
    mock_list_tgz.assert_called_once_with('dummy.tgz')

    mock_is_archive.assert_called_once()
    mock_is_gzip.assert_called_once()
    mock_is_tar.assert_called_once()
    mock_is_tgz.assert_called_once()

def test_list_contents_gzip(mocker):
    """
    Test the test_list_contents for a gzip format archive.
    """
    mock_is_archive = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler.is_archive_format', return_value=True)
    mock_is_tar = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler.is_tar_format', return_value=False)
    mock_is_tgz = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler.is_tgz_format', return_value=False)
    mock_is_gzip = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler.is_gzip_format', return_value=True)
    mock_list_gzip = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler._list_gzip_contents', return_value=['file1.txt'])

    result = ArchiveHandler.list_contents('dummy.gz')
    assert result == ['file1.txt']
    mock_list_gzip.assert_called_once_with('dummy.gz')

    mock_is_archive.assert_called_once()
    mock_is_gzip.assert_called_once()
    mock_is_tar.assert_not_called()
    mock_is_tgz.assert_not_called()

def test_list_contents_unsupported_format(mocker):
    """
    Test the test_list_contents when the format is not supported.
    """
    mock_is_archive = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler.is_archive_format', return_value=False)

    with pytest.raises(TypeError):
        ArchiveHandler.list_contents('unsupported.format')

    mock_is_archive.assert_called_once()

def test_list_contents_unsupported_format_switch(mocker):
    """
    Test the test_list_contents when the format is supported but was not added to the switch statement.
    """
    mock_is_archive = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler.is_archive_format', return_value=True)
    mock_is_tar = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler.is_tar_format', return_value=False)
    mock_is_tgz = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler.is_tgz_format', return_value=False)
    mock_is_gzip = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler.is_gzip_format', return_value=False)

    with pytest.raises(TypeError):
        ArchiveHandler.list_contents('unsupported.format')

    mock_is_archive.assert_called_once()
    mock_is_tar.assert_called_once()
    mock_is_tgz.assert_called_once()
    mock_is_gzip.assert_called_once()

def test_extract_gzip_contents_private_success(mocker):
    """
    Test the _extract_gzip_contents_private method for successful extraction.
    This unit test is mocked and only tests the logic.
    """
    mock_list_contents = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler.list_contents')
    mock_gzip_open = mocker.patch('gradhouse.file.handler.archive_handler.gzip.open')
    mock_path_join = mocker.patch('gradhouse.file.handler.archive_handler.os.path.join')
    mock_open = mocker.patch('gradhouse.file.handler.archive_handler.open')

    source_file_path = 'test_data/archive/gzip_single_file.gz'
    destination_directory = 'test_data/extracted'
    mock_list_contents.return_value = ['file1.txt']
    mock_gzip_open.return_value.__enter__.return_value.read.return_value = b'content'
    mock_path_join.return_value = 'test_data/extracted/file1.txt'

    ArchiveHandler._extract_gzip_contents_private(source_file_path, destination_directory)

    mock_gzip_open.assert_called_once_with(source_file_path, 'rb')
    mock_open.assert_called_once_with('test_data/extracted/file1.txt', 'wb')
    mock_open.return_value.__enter__.return_value.write.assert_called_once_with(b'content')

def test_extract_gzip_contents_private_ioerror_read(mocker):
    """
    Test the _extract_gzip_contents_private method for IOError when the source file cannot be read.
    This unit test is mocked and only tests the logic.
    """
    mock_gzip_open = mocker.patch('gradhouse.file.handler.archive_handler.gzip.open')

    source_file_path = 'test_data/archive/gzip_single_file.gz'
    destination_directory = 'test_data/extracted'
    mock_gzip_open.return_value.__enter__.return_value.read.side_effect = IOError

    with pytest.raises(IOError):
        ArchiveHandler._extract_gzip_contents_private(source_file_path, destination_directory)

def test_extract_tar_or_tgz_contents_private(mocker):
    """
    Test the _extract_tar_or_tgz_contents_private method.
    This unit test is mocked and only tests the logic.
    """
    mock_tarfile_open = mocker.patch('gradhouse.file.handler.archive_handler.tarfile.open')

    source_file_path = 'test.tar'
    destination_directory = 'destination_dir'
    mock_tar = mocker.MagicMock()
    mock_tarfile_open.return_value.__enter__.return_value = mock_tar
    mock_member = mocker.MagicMock()
    mock_member.isfile.return_value = True
    mock_tar.getmembers.return_value = [mock_member]

    ArchiveHandler._extract_tar_or_tgz_contents_private(source_file_path, destination_directory)

    mock_tarfile_open.assert_called_once_with(source_file_path, 'r')
    mock_tar.getmembers.assert_called_once()
    mock_tar.extract.assert_called_once_with(mock_member, destination_directory)

def test_is_extract_possible_source_file_not_found():
    """
    Test the is_extract_possible when the source file is not found.
    """

    # test case: source file not found
    source_file_path = 'this_is_not_a_file'
    destination_directory = TEST_SCRATCH_DIRECTORY
    is_possible = ArchiveHandler.is_extract_possible(source_file_path, destination_directory)
    assert not is_possible

    # test case: source file is a directory
    source_file_path = TEST_DATA_DIRECTORY
    destination_directory = TEST_SCRATCH_DIRECTORY
    is_possible = ArchiveHandler.is_extract_possible(source_file_path, destination_directory)
    assert not is_possible

def test_is_extract_possible_destination_directory_not_found():
    """
    Test the is_extract_possible when the destination directory is not found.
    """

    # test case: destination directory not found
    source_file_path = os.path.join(TEST_DATA_DIRECTORY, 'archive/tar_archive_file.tar')
    destination_directory = 'non_existent_directory'
    is_possible = ArchiveHandler.is_extract_possible(source_file_path, destination_directory)
    assert not is_possible

    # test case: destination directory is a file
    source_file_path = os.path.join(TEST_DATA_DIRECTORY, 'archive/tar_archive_file.tar')
    destination_directory = os.path.join(TEST_DATA_DIRECTORY, 'top_level_text_file.txt')
    is_possible = ArchiveHandler.is_extract_possible(source_file_path, destination_directory)
    assert not is_possible

def test_is_extract_possible_contents_filenames_not_unique(mocker):
    """
    Test the is_extract_possible when the archive filenames are not case-insensitive unique.
    This unit test is partially mocked.
    """

    source_file_path = os.path.join(TEST_DATA_DIRECTORY, 'archive/tar_archive_file.tar')
    destination_directory = TEST_SCRATCH_DIRECTORY
    mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler.list_contents', return_value=['file1.txt', 'File1.txt'])

    is_possible = ArchiveHandler.is_extract_possible(source_file_path, destination_directory)
    assert not is_possible

def test_is_extract_possible_contents_filename_traversal(mocker):
    """
    Test the is_extract_possible when the archive filenames have directory traversal.
    This unit test is partially mocked.
    """

    source_file_path = os.path.join(TEST_DATA_DIRECTORY, 'archive/tar_archive_file.tar')
    destination_directory = TEST_SCRATCH_DIRECTORY
    mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler.list_contents', return_value=['../file1.txt'])

    is_possible = ArchiveHandler.is_extract_possible(source_file_path, destination_directory)
    assert not is_possible

def test_is_extract_possible_destination_file_exists(mocker):
    """
    Test the is_extract_possible when the destination file already exists.
    This unit test is partially mocked.
    """

    source_file_path = os.path.join(TEST_DATA_DIRECTORY, 'archive/tar_archive_file.tar')
    destination_directory = TEST_DATA_DIRECTORY
    mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler.list_contents', return_value=['top_level_text_file.txt'])

    is_possible = ArchiveHandler.is_extract_possible(source_file_path, destination_directory)
    assert not is_possible

def test_is_extract_possible_success(mocker):
    """
    Test the is_extract_possible when successful.
    This unit test is partially mocked.
    """

    source_file_path = os.path.join(TEST_DATA_DIRECTORY, 'archive/tar_archive_file.tar')
    destination_directory = TEST_SCRATCH_DIRECTORY
    mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler.list_contents', return_value=['sample_contents.txt'])

    is_possible = ArchiveHandler.is_extract_possible(source_file_path, destination_directory)
    assert is_possible

def test_extract_contents_not_archive(mocker):
    """
    Test the extract_contents when this is not an archive file.
    """
    # set up the mocks
    mock_is_archive_format = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler.is_archive_format')
    mock_is_gzip_format = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler.is_gzip_format')
    mock_is_tar_format = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler.is_tar_format')
    mock_is_tgz_format = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler.is_tgz_format')

    mock_is_archive_format.return_value = True
    mock_is_gzip_format.return_value = False
    mock_is_tar_format.return_value = False
    mock_is_tgz_format.return_value = False

    # Test unsupported format
    with pytest.raises(TypeError, match='file not listed as a supported archive format'):
        ArchiveHandler.extract_contents('unsupported_format_file', 'destination_directory')

def test_extract_contents_format_not_listed(mocker):
    """
    Test the extract_contents when the format is not in the listed supported types.
    """
    # set up the mock
    mock_is_archive_format = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler.is_archive_format')
    mock_is_archive_format.return_value = False

    # Test not supported archive format
    with pytest.raises(TypeError, match='file not a supported archive format'):
        ArchiveHandler.extract_contents('not_supported_archive_file', 'destination_directory')

def test_extract_contents_gzip(mocker):
    """
    Test the extract_contents for gzip format.
    """
    mock_is_archive = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler.is_archive_format')
    mock_is_gzip = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler.is_gzip_format')
    mock_is_tar = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler.is_tar_format')
    mock_is_tgz = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler.is_tgz_format')
    mock_extract_gzip = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler.extract_gzip_contents')
    mock_extract_tar = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler.extract_tar_contents')
    mock_extract_tgz = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler.extract_tgz_contents')

    mock_is_archive.return_value = True
    mock_is_gzip.return_value = True
    mock_is_tar.return_value = False
    mock_is_tgz.return_value = False

    ArchiveHandler.extract_contents('dummy_path.gz', 'dummy_dest')

    mock_extract_gzip.assert_called_once_with('dummy_path.gz', 'dummy_dest')
    mock_extract_tar.assert_not_called()
    mock_extract_tgz.assert_not_called()

def test_extract_contents_tar(mocker):
    """
    Test the extract_contents for tar format.
    """
    mock_is_archive = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler.is_archive_format')
    mock_is_gzip = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler.is_gzip_format')
    mock_is_tar = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler.is_tar_format')
    mock_is_tgz = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler.is_tgz_format')
    mock_extract_gzip = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler.extract_gzip_contents')
    mock_extract_tar = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler.extract_tar_contents')
    mock_extract_tgz = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler.extract_tgz_contents')

    mock_is_archive.return_value = True
    mock_is_gzip.return_value = False
    mock_is_tar.return_value = True
    mock_is_tgz.return_value = False

    ArchiveHandler.extract_contents('dummy_path.tar', 'dummy_dest')

    mock_extract_tar.assert_called_once_with('dummy_path.tar', 'dummy_dest')
    mock_extract_gzip.assert_not_called()
    mock_extract_tgz.assert_not_called()

def test_extract_contents_tgz(mocker):
    """
    Test the extract_contents for tgz format.
    """
    mock_is_archive = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler.is_archive_format')
    mock_is_gzip = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler.is_gzip_format')
    mock_is_tar = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler.is_tar_format')
    mock_is_tgz = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler.is_tgz_format')
    mock_extract_gzip = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler.extract_gzip_contents')
    mock_extract_tar = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler.extract_tar_contents')
    mock_extract_tgz = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler.extract_tgz_contents')

    mock_is_archive.return_value = True
    mock_is_gzip.return_value = False
    mock_is_tar.return_value = False
    mock_is_tgz.return_value = True

    ArchiveHandler.extract_contents('dummy_path.tgz', 'dummy_dest')

    mock_extract_tgz.assert_called_once_with('dummy_path.tgz', 'dummy_dest')
    mock_extract_gzip.assert_not_called()
    mock_extract_tar.assert_not_called()

def test_extract_gzip_contents_success(mocker):
    """
    Test the extract_gzip_contents method when extraction is possible.
    This method is fully mocked to test the control flow only.
    """
    mock_is_gzip = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler.is_gzip_format')
    mock_is_extract = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler.is_extract_possible')
    mock_extract_gzip = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler._extract_gzip_contents_private')

    mock_is_gzip.return_value = True
    mock_is_extract.return_value = True

    source_file_path = os.path.join(TEST_DATA_DIRECTORY, 'archive/gzip_single_file.gz')
    destination_directory = TEST_SCRATCH_DIRECTORY

    # Call the method under test
    ArchiveHandler.extract_gzip_contents(source_file_path, destination_directory)

    # Assert the mocks were called with the correct arguments
    mock_is_gzip.assert_called_once_with(source_file_path)
    mock_is_extract.assert_called_once_with(source_file_path, destination_directory)
    mock_extract_gzip.assert_called_once_with(source_file_path, destination_directory)

def test_extract_gzip_contents_not_gzip_format(mocker):
    """
    Test the extract_gzip_contents method when the file is not in gzip format.
    This method is fully mocked to test the control flow only.
    """
    mock_is_gzip = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler.is_gzip_format')
    mock_is_extract = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler.is_extract_possible')
    mock_extract_gzip = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler._extract_gzip_contents_private')

    mock_is_gzip.return_value = False
    mock_is_extract.return_value = True

    source_file_path = os.path.join(TEST_DATA_DIRECTORY, 'archive/gzip_single_file.gz')
    destination_directory = TEST_SCRATCH_DIRECTORY

    # Call the method under test
    with pytest.raises(TypeError, match='file not in gzip archive format'):
        ArchiveHandler.extract_gzip_contents(source_file_path, destination_directory)

    # Assert the mocks were called with the correct arguments
    mock_is_gzip.assert_called_once_with(source_file_path)
    mock_is_extract.assert_not_called()
    mock_extract_gzip.assert_not_called()

def test_extract_gzip_contents_extract_not_possible(mocker):
    """
    Test the extract_gzip_contents method when the archive cannot be extracted.
    This method is fully mocked to test the control flow only.
    """
    mock_is_gzip = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler.is_gzip_format')
    mock_is_extract = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler.is_extract_possible')
    mock_extract_gzip = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler._extract_gzip_contents_private')

    mock_is_gzip.return_value = True
    mock_is_extract.return_value = False

    source_file_path = os.path.join(TEST_DATA_DIRECTORY, 'archive/gzip_single_file.gz')
    destination_directory = TEST_SCRATCH_DIRECTORY

    # Call the method under test
    with pytest.raises(ValueError, match='extraction not possible'):
        ArchiveHandler.extract_gzip_contents(source_file_path, destination_directory)

    # Assert the mocks were called with the correct arguments
    mock_is_gzip.assert_called_once_with(source_file_path)
    mock_is_extract.assert_called_once_with(source_file_path, destination_directory)
    mock_extract_gzip.assert_not_called()

def test_extract_tgz_contents_success(mocker):
    """
    Test the extract_tgz_contents method when extraction is possible.
    This method is fully mocked to test the control flow only.
    """
    mock_is_tgz = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler.is_tgz_format')
    mock_is_extract = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler.is_extract_possible')
    mock_extract_tar_or_tgz = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler._extract_tar_or_tgz_contents_private')

    mock_is_tgz.return_value = True
    mock_is_extract.return_value = True

    source_file_path = os.path.join(TEST_DATA_DIRECTORY, 'archive/tgz_archive_file.gz')
    destination_directory = TEST_SCRATCH_DIRECTORY

    # Call the method under test
    ArchiveHandler.extract_tgz_contents(source_file_path, destination_directory)

    # Assert the mocks were called with the correct arguments
    mock_is_tgz.assert_called_once_with(source_file_path)
    mock_is_extract.assert_called_once_with(source_file_path, destination_directory)
    mock_extract_tar_or_tgz.assert_called_once_with(source_file_path, destination_directory)

def test_extract_tgz_contents_not_tgz_format(mocker):
    """
    Test the extract_tgz_contents method when the file is not in tgz format.
    This method is fully mocked to test the control flow only.
    """
    mock_is_tgz = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler.is_tgz_format')
    mock_is_extract = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler.is_extract_possible')
    mock_extract_tar_or_tgz = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler._extract_tar_or_tgz_contents_private')

    mock_is_tgz.return_value = False
    mock_is_extract.return_value = True

    source_file_path = os.path.join(TEST_DATA_DIRECTORY, 'archive/tgz_archive_file.gz')
    destination_directory = TEST_SCRATCH_DIRECTORY

    # Call the method under test
    with pytest.raises(TypeError, match='file not in tgz archive format'):
        ArchiveHandler.extract_tgz_contents(source_file_path, destination_directory)

    # Assert the mocks were called with the correct arguments
    mock_is_tgz.assert_called_once_with(source_file_path)
    mock_is_extract.assert_not_called()
    mock_extract_tar_or_tgz.assert_not_called()

def test_extract_tgz_contents_extract_not_possible(mocker):
    """
    Test the extract_tgz_contents method when the archive cannot be extracted.
    This method is fully mocked to test the control flow only.
    """
    mock_is_tgz = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler.is_tgz_format')
    mock_is_extract = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler.is_extract_possible')
    mock_extract_tar_or_tgz = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler._extract_tar_or_tgz_contents_private')

    mock_is_tgz.return_value = True
    mock_is_extract.return_value = False

    source_file_path = os.path.join(TEST_DATA_DIRECTORY, 'archive/tgz_archive_file.gz')
    destination_directory = TEST_SCRATCH_DIRECTORY

    # Call the method under test
    with pytest.raises(ValueError, match='extraction not possible'):
        ArchiveHandler.extract_tgz_contents(source_file_path, destination_directory)

    # Assert the mocks were called with the correct arguments
    mock_is_tgz.assert_called_once_with(source_file_path)
    mock_is_extract.assert_called_once_with(source_file_path, destination_directory)
    mock_extract_tar_or_tgz.assert_not_called()

def test_extract_tar_contents_success(mocker):
    """
    Test the extract_tar_contents method when extraction is possible.
    This method is fully mocked to test the control flow only.
    """
    mock_is_tar = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler.is_tar_format')
    mock_is_extract = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler.is_extract_possible')
    mock_extract_tar_or_tgz = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler._extract_tar_or_tgz_contents_private')

    mock_is_tar.return_value = True
    mock_is_extract.return_value = True

    source_file_path = os.path.join(TEST_DATA_DIRECTORY, 'archive/tar_archive_file.gz')
    destination_directory = TEST_SCRATCH_DIRECTORY

    # Call the method under test
    ArchiveHandler.extract_tar_contents(source_file_path, destination_directory)

    # Assert the mocks were called with the correct arguments
    mock_is_tar.assert_called_once_with(source_file_path)
    mock_is_extract.assert_called_once_with(source_file_path, destination_directory)
    mock_extract_tar_or_tgz.assert_called_once_with(source_file_path, destination_directory)

def test_extract_tar_contents_not_tar_format(mocker):
    """
    Test the extract_tar_contents method when the file is not in tar format.
    This method is fully mocked to test the control flow only.
    """
    mock_is_tar = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler.is_tar_format')
    mock_is_extract = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler.is_extract_possible')
    mock_extract_tar_or_tgz = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler._extract_tar_or_tgz_contents_private')

    mock_is_tar.return_value = False
    mock_is_extract.return_value = True

    source_file_path = os.path.join(TEST_DATA_DIRECTORY, 'archive/tar_archive_file.gz')
    destination_directory = TEST_SCRATCH_DIRECTORY

    # Call the method under test
    with pytest.raises(TypeError, match='file not in tar archive format'):
        ArchiveHandler.extract_tar_contents(source_file_path, destination_directory)

    # Assert the mocks were called with the correct arguments
    mock_is_tar.assert_called_once_with(source_file_path)
    mock_is_extract.assert_not_called()
    mock_extract_tar_or_tgz.assert_not_called()

def test_extract_tar_contents_extract_not_possible(mocker):
    """
    Test the extract_tar_contents method when the archive cannot be extracted.
    This method is fully mocked to test the control flow only.
    """
    mock_is_tar = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler.is_tar_format')
    mock_is_extract = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler.is_extract_possible')
    mock_extract_tar_or_tgz = mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler._extract_tar_or_tgz_contents_private')

    mock_is_tar.return_value = True
    mock_is_extract.return_value = False

    source_file_path = os.path.join(TEST_DATA_DIRECTORY, 'archive/tar_archive_file.gz')
    destination_directory = TEST_SCRATCH_DIRECTORY

    # Call the method under test
    with pytest.raises(ValueError, match='extraction not possible'):
        ArchiveHandler.extract_tar_contents(source_file_path, destination_directory)

    # Assert the mocks were called with the correct arguments
    mock_is_tar.assert_called_once_with(source_file_path)
    mock_is_extract.assert_called_once_with(source_file_path, destination_directory)
    mock_extract_tar_or_tgz.assert_not_called()

def make_gzip_file_with_flags(tmp_path, flags, filename=None):
    file_path = tmp_path / "test.gz"
    with open(file_path, "wb") as f:
        # Write gzip header
        id1, id2 = 0x1F, 0x8B
        compression = 0x08
        mtime = 0
        extra_flags = 0
        os_id = 255
        f.write(struct.pack("<BBBBLBB", id1, id2, compression, flags, mtime, extra_flags, os_id))
        # Optionally write filename field
        if flags & 0x08 and filename:
            f.write(filename.encode() + b"\0")
        # Write minimal compressed data
        f.write(b'\x03\x00')  # minimal deflate block
        f.write(b'\x00' * 8)  # CRC32 and ISIZE
    return str(file_path)

def test_list_gzip_contents_filename_field_present_and_absent(tmp_path):
    # Case 1: filename field present
    file_with_name = make_gzip_file_with_flags(tmp_path, flags=0x08, filename="myfile.txt")
    result = ArchiveHandler._list_gzip_contents(file_with_name)
    assert result == ["myfile.txt"]

    # Case 2: filename field absent
    file_without_name = make_gzip_file_with_flags(tmp_path, flags=0x00)
    result = ArchiveHandler._list_gzip_contents(file_without_name)
    assert result == []

def test_list_gzip_contents_invalid_compression_format(tmp_path, monkeypatch):
    # Patch is_gzip_format to return True so we get past that check
    monkeypatch.setattr(ArchiveHandler, "is_gzip_format", lambda x: True)

    # Create a file with an invalid gzip header (wrong id1, id2, or compression)
    invalid_gzip = tmp_path / "invalid.gz"
    with open(invalid_gzip, "wb") as f:
        # id1, id2, compression, flags, mtime, extra_flags, os_id
        f.write(struct.pack("<BBBBLBB", 0x00, 0x00, 0x00, 0, 0, 0, 0))
        f.write(b'\x00' * 10)  # pad file

    # Should not raise, just return empty list
    result = ArchiveHandler._list_gzip_contents(str(invalid_gzip))
    assert result == []

@pytest.mark.parametrize("source_file_path, destination_directory, expected_errors", [
    # Source file not found
    ('this_is_not_a_file', TEST_SCRATCH_DIRECTORY, ['file not found']),
    # Source file is a directory
    (os.path.dirname(__file__), TEST_SCRATCH_DIRECTORY, ['file not found']),
    # Destination directory not found
    (os.path.join(TEST_DATA_DIRECTORY, 'archive/tar_archive_file.tar'), 'non_existent_directory', ['destination directory not found']),
    # Destination directory is a file
    (os.path.join(TEST_DATA_DIRECTORY, 'archive/tar_archive_file.tar'),
     os.path.join(TEST_DATA_DIRECTORY, 'top_level_text_file.txt'),
     ['destination directory not found']),
])
def test_check_extract_possible_file_or_dir_not_found(source_file_path, destination_directory, expected_errors):
    """
    Test check_extract_possible for file or directory not found cases.
    """
    errors = ArchiveHandler.check_extract_possible(source_file_path, destination_directory)
    assert errors == expected_errors

def test_check_extract_possible_contents_filenames_not_unique(mocker):
    """
    Test check_extract_possible when archive filenames are not case-insensitive unique.
    """
    source_file_path = os.path.join(TEST_DATA_DIRECTORY, 'archive/tar_archive_file.tar')
    destination_directory = TEST_SCRATCH_DIRECTORY
    mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler.list_contents', return_value=['file1.txt', 'File1.txt'])

    errors = ArchiveHandler.check_extract_possible(source_file_path, destination_directory)
    assert 'archive contents filename is not unique on case-insensitive file systems' in errors

def test_check_extract_possible_contents_filename_traversal(mocker):
    """
    Test check_extract_possible when archive filenames have directory traversal.
    """
    source_file_path = os.path.join(TEST_DATA_DIRECTORY, 'archive/tar_archive_file.tar')
    destination_directory = TEST_SCRATCH_DIRECTORY
    mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler.list_contents', return_value=['../file1.txt'])

    errors = ArchiveHandler.check_extract_possible(source_file_path, destination_directory)
    assert 'archive contents filenames are forbidden' in errors

def test_check_extract_possible_destination_file_exists(mocker):
    """
    Test check_extract_possible when the destination file already exists.
    """
    source_file_path = os.path.join(TEST_DATA_DIRECTORY, 'archive/tar_archive_file.tar')
    destination_directory = TEST_DATA_DIRECTORY
    mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler.list_contents', return_value=['top_level_text_file.txt'])

    errors = ArchiveHandler.check_extract_possible(source_file_path, destination_directory)
    assert 'destination file already exists' in errors

def test_check_extract_possible_success(mocker):
    """
    Test check_extract_possible when extraction is possible (no errors).
    """
    source_file_path = os.path.join(TEST_DATA_DIRECTORY, 'archive/tar_archive_file.tar')
    destination_directory = TEST_SCRATCH_DIRECTORY
    mocker.patch('gradhouse.file.handler.archive_handler.ArchiveHandler.list_contents', return_value=['sample_contents.txt'])

    errors = ArchiveHandler.check_extract_possible(source_file_path, destination_directory)
    assert errors == []