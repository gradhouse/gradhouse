# File: test_file_name.py
# Description: Unit tests for the FileName class.
#
# Copyright (c) 2025 Jason Stuber
# Licensed under the MIT License. See the LICENSE file for more details.

import pytest
from gradhouse.file.file_name import FileName


@pytest.mark.parametrize("filename, expected_extension", [
    ('example.txt', '.txt'),
    ('archive.tar.gz', '.gz'),
    ('README', ''),
    ('.gitignore', ''),
    ('/path/to/file/example.txt', '.txt'),
    ('', '')
])
def test_get_file_extension(filename, expected_extension):
    """
    Test get_file_extension method
    """
    assert FileName.get_file_extension(filename) == expected_extension

@pytest.mark.parametrize("filename, expected_basename", [
    ('example.txt', 'example.txt'),
    ('archive.tar.gz', 'archive.tar.gz'),
    ('README', 'README'),
    ('.gitignore', '.gitignore'),
    ('/path/to/file/example.txt', 'example.txt'),
    ('', '')
])
def test_get_file_basename(filename, expected_basename):
    """
    Test get_file_basename method
    """
    assert FileName.get_file_basename(filename) == expected_basename

@pytest.mark.parametrize("path", [
    "valid_filename.txt",
    "another_valid-file+name=1.txt",
    "valid/filename/with/dirs.txt"
])
def test_is_file_characters_allowed_valid(path):
    """
    Test is_file_characters_allowed method when the file path has valid characters
    """
    assert FileName.is_path_characters_allowed(path)

@pytest.mark.parametrize("path", [
    "invalid/filename/with/..",
    "invalid/filename/with/../dirs.txt",
    "invalid/filename/with/empty//component.txt",
    "invalid/filename/with/illegal|char.txt",
    "invalid/filename/with/illegal<chars>.txt",
    "",
    ".",
    "/root/file.txt"
])
def test_is_file_characters_allowed_invalid(path):
    """
    Test is_path_characters_allowed method when the file path has invalid characters.
    """
    assert not FileName.is_path_characters_allowed(path)

@pytest.mark.parametrize("directory_path, combined_path, expected_is_within", [
    ('/home/user', '/home/user/file.txt', True),
    ('/home/user', '/home/user/subdir/file.txt', True),
    ('/home/user', '/home/otheruser/file.txt', False),
    ('/home/user', '/home/user/../otheruser/file.txt', False),
    ('/home/user', '/home/user', True),
    ('/home/user', '/home/user/..', False),
    ('/home/user', '/home/user/../user2', False)
])
def test_is_path_within_directory_linux(directory_path, combined_path, expected_is_within):
    """
    Test is_path_within_directory method for Linux-like systems
    """
    assert FileName.is_path_within_directory(directory_path, combined_path) == expected_is_within

@pytest.mark.parametrize("filename", [
    '../etc/passwd',
    '/etc/passwd',
    '..\\etc\\passwd',
    'temp/../../etc/passwd'
])
def test_is_filename_allowed_with_traversal_attack(filename):
    """
    Test is_filename_allowed method for traversal attacks.
    """
    assert not FileName.is_filename_allowed(filename)

@pytest.mark.parametrize("filename", [
    'file_with_@_char',
    'file_with_#_char',
    'file_with_$$_char',
    'file_with_&_char'
])
def test_is_filename_allowed_with_disallowed_characters(filename):
    """
    Test the is_filename_allowed method for disallowed characters.
    """
    assert not FileName.is_filename_allowed(filename)

@pytest.mark.parametrize("filename", [
    'file_with_underscore',
    'file-with-dash',
    'file.with.period',
    'file+with+plus',
    'file=with=equals'
])
def test_is_filename_allowed_with_allowed_characters(filename):
    """
    Test the is_filename_allowed method for allowed characters.
    """
    assert FileName.is_filename_allowed(filename)

@pytest.mark.parametrize("filename", [
    'file//name',
    '/file/name/',
    'file/./name'
])
def test_is_filename_allowed_with_empty_components(filename):
    """
    Test the is_filename_allowed method for empty components.
    """
    assert not FileName.is_filename_allowed(filename)

@pytest.mark.parametrize("filename", [
    'file/../name',
    'file/..',
    '../file/name',
    'file/./name',
    'file/.',
    './file/name'
])
def test_is_filename_allowed_with_dots(filename):
    """
    Test the is_filename_allowed method for single and double dots.
    """
    assert not FileName.is_filename_allowed(filename)

@pytest.mark.parametrize("filename, expected", [
    ('', False),
    (FileName.MAX_FILENAME_LENGTH * 'f', False),
    ((FileName.MAX_FILENAME_LENGTH - 1) * 'f', True)
])
def test_is_filename_allowed_with_file_length(filename, expected):
    """
    Test the is_filename_allowed method when the file length is too short or too long.
    """
    assert FileName.is_filename_allowed(filename) == expected

@pytest.mark.parametrize("filenames, is_case_insensitive, is_filename_only, expected", [
    (['file.txt', 'File.txt', 'File.TXT'], False, True, True),
    (['directory/file.txt', 'Directory/file.txt', 'DIRECTORY/file.txt'], False, True, False),
    (['file.txt', 'File2.txt', 'File3.TXT'], True, True, True),
    (['file.txt', 'File.txt', 'File.TXT'], True, True, False),
    (['directory1/file.txt', 'Directory2/file.txt', 'DIRECTORY3/file.txt'], True, False, True),
    (['file.txt', 'File2.txt', 'File3.TXT'], True, False, True),
    (['file.txt', 'File.txt', 'File.TXT'], True, False, False),
    (['directory/file.txt', 'Directory/file.txt', 'DIRECTORY/file.txt'], True, False, False)
])
def test_is_filename_list_unique(filenames, is_case_insensitive, is_filename_only, expected):
    """
    Test the is_filename_list_unique method
    """
    assert FileName.is_filename_list_unique(filenames, is_case_insensitive, is_filename_only) == expected
