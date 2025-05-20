# File: registry.py
# Description: Generic base class for maintaining a registry of entries identified by unique keys.
#
# Copyright (c) 2025 Jason Stuber
# Licensed under the MIT License. See the LICENSE file for more details.

import copy

class Registry:
    """
    Generic base class for maintaining a registry of entries identified by unique keys.
    """

    def __init__(self) -> None:
        """
        Initializes the registry as an empty dictionary.
        """
        self._registry = dict()

    def clear(self) -> None:
        """
        Clears the registry and resets it to its default state.
        """
        self._registry.clear()

    def is_key_present(self, hash_key: str) -> bool:
        """
        Determine if the given hash key is present in the registry.

        :param hash_key: str, the hash key to check.
        :return: bool, True if the hash key is present, False otherwise.
        """
        return hash_key in self._registry

    def get_entry(self, hash_key: str) -> dict:
        """
        Retrieve the entry associated with the given hash key.

        :param hash_key: str, the hash key to look up.
        :return: The entry if found.
        :raises KeyError: If the hash key is not present in the registry.
        """
        if hash_key not in self._registry:
            raise KeyError(f"Hash key '{hash_key}' not found in registry.")
        return copy.deepcopy(self._registry[hash_key])

    def add_entry(self, hash_key: str, entry: dict) -> None:
        """
        Add a new entry to the registry.

        :param hash_key: str, the unique key for the entry.
        :param entry: dict, the entry data.

        :raises KeyError: If the key already exists.
        """
        if hash_key in self._registry:
            raise KeyError(f"Hash key '{hash_key}' already exists in registry.")

        self._registry[hash_key] = copy.deepcopy(entry)

    def update_entry(self, hash_key: str, entry: dict) -> None:
        """
        Update an existing entry in the registry.

        :param hash_key: str, the unique key for the entry.
        :param entry: dict, the new entry data.
        :raises KeyError: If the key does not exist.
        """
        if hash_key not in self._registry:
            raise KeyError(f"Hash key '{hash_key}' not found in registry.")

        self._registry[hash_key] = copy.deepcopy(entry)

    def delete_entry(self, hash_key: str) -> None:
        """
        Delete an entry from the registry.

        :param hash_key: str, the unique key for the entry.

        :raises KeyError: If the key does not exist.
        """
        if hash_key not in self._registry:
            raise KeyError(f"Hash key '{hash_key}' not found in registry.")

        del self._registry[hash_key]

    def list_keys(self) -> list[str]:
        """
        Return a list of all keys in the registry.
        """
        return list(self._registry.keys())

    def __len__(self):
        """
        Return the number of entries in the registry.
        """
        return len(self._registry)
