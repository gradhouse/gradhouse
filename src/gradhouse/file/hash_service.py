# File: hash_service.py
# Description: Hash services.
#
# Copyright (c) 2025 Jason Stuber
# Licensed under the MIT License. See the LICENSE file for more details.

from enum import Enum
import os
from hashlib import md5, sha256, sha512, sha3_512


class HashType(Enum):
    """
    Hash encoding categories.

    This enumeration is used to specify hash types.

    Attributes:
        HASH_TYPE_MD5: Represents the MD5 hash type.
        HASH_TYPE_SHA256: Represents the SHA256 hash type.
        HASH_TYPE_SHA512: Represents the SHA512 hash type.
        HASH_TYPE_SHA3_512: Represents the SHA3_512 hash type.
    """

    HASH_TYPE_MD5 = 'MD5'
    HASH_TYPE_SHA256 = 'SHA256'
    HASH_TYPE_SHA512= 'SHA512'
    HASH_TYPE_SHA3_512 = 'SHA3_512'


class HashService:
    """
    A class to generate hash values.
    """

    _hash_type_encoder_map = {
        HashType.HASH_TYPE_MD5: md5,
        HashType.HASH_TYPE_SHA256: sha256,
        HashType.HASH_TYPE_SHA512: sha512,
        HashType.HASH_TYPE_SHA3_512: sha3_512
    }

    @staticmethod
    def is_hash_type_allowed(hash_type: HashType) -> bool:
        """
        Check if the given hash type is allowed.

        :param hash_type: HashType, hash type category such as MD5 or SHA256
        :return: bool, True if the hash type is allowed, False otherwise
        """

        is_encoder_available = (hash_type in HashService._hash_type_encoder_map)
        return is_encoder_available

    @staticmethod
    def _get_hash_encoder_instance(hash_type: HashType):
        """
        Get an instance of the hash encoder for the given hash type.

        :param hash_type: HashType, hash type category such as MD5 or SHA256
        :return: _Hash, instance of the hash encoder

        :raises ValueError: if the hash type does not match a supported encoder
        """

        is_encoder_available = HashService.is_hash_type_allowed(hash_type)
        if not is_encoder_available:
            raise ValueError('hash type must be an allowed value')

        hash_encoder = HashService._hash_type_encoder_map[hash_type]()

        return hash_encoder

    @staticmethod
    def calculate_file_hash(file_path: str, hash_type: HashType, file_buffer_size: int=65536) -> str:
        """
        Calculate the hash for the given file.

        :param file_path: str, path to the file
        :param hash_type: HashType, hash type category such as MD5 or SHA256
        :param file_buffer_size: int, size of the file buffer for block encoding, 65536 default
        :return: str, hash value as a hexadecimal hash key

        :raises ValueError: if the file buffer size is invalid
        :raises ValueError: if the hash type does not match a supported encoder
        :raises FileNotFoundError: If the file is not found.
        """

        if file_buffer_size <= 0:
            raise ValueError('buffer size must be positive')

        is_encoder_available = HashService.is_hash_type_allowed(hash_type)
        if not is_encoder_available:
            raise ValueError('hash type must be an allowed value')

        is_file_found = os.path.isfile(file_path)
        if not is_file_found:
            raise FileNotFoundError('file not found')

        hash_encoder = HashService._get_hash_encoder_instance(hash_type)

        with open(file_path, 'rb') as file_handle:
            is_reading = True
            while is_reading:
                buffer = file_handle.read(file_buffer_size)

                if not buffer:
                    is_reading = False
                else:
                    hash_encoder.update(buffer)

            hash_value = hash_encoder.hexdigest()

        return hash_value

    @staticmethod
    def calculate_buffer_hash(buffer: bytes, hash_type: HashType) -> str:
        """
        Calculate the hash for the given binary buffer

        :param buffer: str, binary buffer
        :param hash_type: HashType, hash type category such as MD5 or SHA256
        :return: str, hash value as a hexadecimal hash key

        :raises ValueError: if the hash type does not match a supported encoder
        """

        is_encoder_available = HashService.is_hash_type_allowed(hash_type)

        if not is_encoder_available:
            raise ValueError('hash type must be an allowed value')

        hash_encoder = HashService._get_hash_encoder_instance(hash_type)
        hash_encoder.update(buffer)
        hash_value = hash_encoder.hexdigest()

        return hash_value
