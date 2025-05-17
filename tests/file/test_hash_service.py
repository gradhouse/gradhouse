# File: test_hash_service.py
# Description: Unit tests for the HashType and HashService classes.
#
# Copyright (c) 2025 Jason Stuber
# Licensed under the MIT License. See the LICENSE file for more details.

from hashlib import md5, sha256, sha512, sha3_512
import os
import pytest
import tempfile

from gradhouse.file.hash_service import HashType, HashService


# Test for HashType
def test_enum():
    """
    Test that the value of the enumeration has the expected value.
    """
    assert HashType.HASH_TYPE_MD5.value == 'MD5'
    assert HashType.HASH_TYPE_SHA256.value == 'SHA256'
    assert HashType.HASH_TYPE_SHA512.value == 'SHA512'
    assert HashType.HASH_TYPE_SHA3_512.value == 'SHA3_512'

def test_enum_unchanged():
    """
    Test that the enum values have not been extended.
    """
    assert len(HashType) == 4

# Test for HashService
TEST_DIRECTORY = os.path.dirname(os.path.dirname(__file__))
TEST_DATA_DIRECTORY = os.path.join(TEST_DIRECTORY, 'test_data')

@pytest.mark.parametrize("hash_type_category, expected_is_allowed", [
    (HashType.HASH_TYPE_MD5, True),
    (HashType.HASH_TYPE_SHA256, True),
    (HashType.HASH_TYPE_SHA512, True),
    (HashType.HASH_TYPE_SHA3_512, True),
    (1337, False),
])
def test_is_hash_type_allowed(hash_type_category, expected_is_allowed):
    """
    Test the is_hash_type_allowed method.
    """
    assert HashService.is_hash_type_allowed(hash_type_category) == expected_is_allowed

@pytest.mark.parametrize("hash_type_category, expected_encoder, expected_encoder_name", [
    (HashType.HASH_TYPE_MD5, md5(), 'md5'),
    (HashType.HASH_TYPE_SHA256, sha256(), 'sha256'),
    (HashType.HASH_TYPE_SHA512, sha512(), 'sha512'),
    (HashType.HASH_TYPE_SHA3_512, sha3_512(), 'sha3_512'),
])
def test_get_hash_encoder_instance(hash_type_category, expected_encoder, expected_encoder_name):
    """
    Test the _get_hash_encoder_instance method.
    """
    encoder = HashService._get_hash_encoder_instance(hash_type_category)
    assert isinstance(encoder, type(expected_encoder))
    assert encoder.name == expected_encoder_name

def test_get_hash_encoder_instance_raise_hash_type_category_unknown():
    """
    Test the _get_hash_encoder_instance method when the hash type category is unknown.
    """
    with pytest.raises(ValueError):
        HashService._get_hash_encoder_instance(1337)

@pytest.mark.parametrize("hash_type_category, expected_hash_key", [
    (HashType.HASH_TYPE_MD5, 'ca9cd1e1b779a6c53da222067617f329'),
    (HashType.HASH_TYPE_SHA256, '730d388b796882f7ae83e0733272094f491b276da07c06372e1d87e19f8190a7'),
    (HashType.HASH_TYPE_SHA512, 'cc532caf6ee7cfd28e9fd510f25b3137e872676b78879a439418c3f997123d03'
                                '31bdb6aa65fad3c3fded2a825078c13f4ef62b2b0e229d22db825833a8a5f6f8'),
    (HashType.HASH_TYPE_SHA3_512, 'd0aea0ad35f929cfefadda45a1a5f582f435ef21fdc55a505be59e51fd54c1'
                                  '70b1eb7ef9512db04ec1251288c034062e2e7da59cab7c22f949dd0d6da4bde9ad'),
])
def test_calculate_file_hash_all_hash_types(hash_type_category, expected_hash_key):
    """
    Test the calculate_file_hash method for all specified hash types.
    """
    test_content = b"This is a test file content for hashing."
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(test_content)
        temp_file_path = temp_file.name

    try:
        hash_key = HashService.calculate_file_hash(temp_file_path, hash_type_category)
        assert hash_key == expected_hash_key
    finally:
        os.remove(temp_file_path)

@pytest.mark.parametrize("buffer_size", [None, 256, 1024, 16384, 32768, 65536])
def test_calculate_file_hash_all_buffer_sizes(buffer_size):
    """
    Test the calculate_file_hash method for a range of buffer sizes.
    """
    test_content = b"This is a test file content for hashing."
    expected_key_sha_256 = '730d388b796882f7ae83e0733272094f491b276da07c06372e1d87e19f8190a7'

    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(test_content)
        temp_file_path = temp_file.name

    try:
        if buffer_size is None:
            hash_key = HashService.calculate_file_hash(temp_file_path, HashType.HASH_TYPE_SHA256)
        else:
            hash_key = HashService.calculate_file_hash(temp_file_path, HashType.HASH_TYPE_SHA256, file_buffer_size=buffer_size)
        assert hash_key == expected_key_sha_256
    finally:
        os.remove(temp_file_path)

@pytest.mark.parametrize("file_buffer_size", [0, -1])
def test_calculate_file_hash_raise_file_buffer_size_not_positive(file_buffer_size):
    """
    Test the calculate_file_hash method when the file buffer size is not positive.
    """
    valid_file_path = os.path.join(TEST_DATA_DIRECTORY, 'txt/text_file.txt')
    valid_hash_type = HashType.HASH_TYPE_MD5
    with pytest.raises(ValueError):
        HashService.calculate_file_hash(valid_file_path, valid_hash_type, file_buffer_size=file_buffer_size)

def test_calculate_file_hash_raise_hash_type_unknown():
    """
    Test the calculate_file_hash method when the hash type is unknown.
    """
    valid_file_path = os.path.join(TEST_DATA_DIRECTORY, 'text_file.txt')
    valid_buffer_size = 65536

    with pytest.raises(ValueError):
        HashService.calculate_file_hash(valid_file_path, 1337)

    with pytest.raises(ValueError):
        HashService.calculate_file_hash(valid_file_path, 1337, file_buffer_size=valid_buffer_size)

@pytest.mark.parametrize("filename", [
    TEST_DATA_DIRECTORY,
    os.path.join(TEST_DATA_DIRECTORY, 'not_found_text_file.txt'),
])
def test_calculate_file_hash_raise_file_not_found(filename):
    """
    Test the calculate_file_hash method when the file is not found or the path directs to a non-file.
    """
    valid_hash_type = HashType.HASH_TYPE_MD5
    valid_buffer_size = 65536

    with pytest.raises(FileNotFoundError):
        HashService.calculate_file_hash(filename, valid_hash_type)

    with pytest.raises(FileNotFoundError):
        HashService.calculate_file_hash(filename, valid_hash_type, file_buffer_size=valid_buffer_size)

@pytest.mark.parametrize("hash_type_category, expected_hash_key", [
    (HashType.HASH_TYPE_MD5, 'ca9cd1e1b779a6c53da222067617f329'),
    (HashType.HASH_TYPE_SHA256, '730d388b796882f7ae83e0733272094f491b276da07c06372e1d87e19f8190a7'),
    (HashType.HASH_TYPE_SHA512, 'cc532caf6ee7cfd28e9fd510f25b3137e872676b78879a439418c3f997123d03'
                                '31bdb6aa65fad3c3fded2a825078c13f4ef62b2b0e229d22db825833a8a5f6f8'),
    (HashType.HASH_TYPE_SHA3_512, 'd0aea0ad35f929cfefadda45a1a5f582f435ef21fdc55a505be59e51fd54c1'
                                  '70b1eb7ef9512db04ec1251288c034062e2e7da59cab7c22f949dd0d6da4bde9ad'),
])
def test_calculate_buffer_hash(hash_type_category, expected_hash_key):
    """
    Test the calculate_buffer_hash method for all specified hash types.
    """

    buffer = b"This is a test file content for hashing."
    hash_key = HashService.calculate_buffer_hash(buffer, hash_type_category)
    assert hash_key == expected_hash_key

def test_calculate_buffer_hash_raise_hash_type_unknown():
    """
    Test the calculate_buffer_hash method when the hash type is unknown.
    """
    test_content = b"This is a test file content for hashing."
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(test_content)
        temp_file_path = temp_file.name

    try:
        with open(temp_file_path, 'rb') as file_handle:
            buffer = file_handle.read()

        with pytest.raises(ValueError):
            HashService.calculate_buffer_hash(buffer, 1337)
    finally:
        os.remove(temp_file_path)
