# File: test_registry.py
# Description: Unit tests for the Registry base class.
#
# Copyright (c) 2025 Jason Stuber
# Licensed under the MIT License. See the LICENSE file for more details.

import pytest
from gradhouse.registry.registry import Registry

def test_registry_initialization():
    """
    Test that Registry initializes with an empty _registry dictionary.
    """
    reg = Registry()
    assert isinstance(reg._registry, dict)
    assert reg._registry == {}

def test_registry_clear():
    """
    Test that Registry.clear() empties the _registry dictionary.
    """
    reg = Registry()
    reg._registry['test'] = 'value'
    assert reg._registry != {}
    reg.clear()
    assert reg._registry == {}

@pytest.fixture
def registry():
    """Fixture to provide a Registry with two keys."""
    reg = Registry()
    reg._registry = {"abc123": {"foo": 1}, "def456": {"bar": 2}}
    return reg

def test_is_key_present_true(registry):
    """
    Test that is_key_present returns True when the hash key exists in the registry.
    """
    assert registry.is_key_present("abc123") is True

def test_is_key_present_false(registry):
    """
    Test that is_key_present returns False when the hash key does not exist in the registry.
    """
    assert registry.is_key_present("notfound") is False

def test_is_key_present_empty_registry():
    """
    Test that is_key_present returns False when the registry is empty.
    """
    reg = Registry()
    assert reg.is_key_present("abc123") is False

def test_get_entry_returns_deepcopy():
    """
    Test that get_entry returns a deep copy of the entry in Registry.
    """
    reg = Registry()
    reg._registry["key1"] = {"a": 1, "b": {"c": 2}}
    entry = reg.get_entry("key1")
    assert entry == {"a": 1, "b": {"c": 2}}
    entry["b"]["c"] = 99
    assert reg._registry["key1"]["b"]["c"] == 2

def test_get_entry_keyerror():
    """
    Test that get_entry raises KeyError if the hash key is not present in Registry.
    """
    reg = Registry()
    with pytest.raises(KeyError):
        reg.get_entry("missing_key")

def test_add_entry_and_get_entry():
    """
    Test adding a new entry and retrieving it.
    """
    reg = Registry()
    reg.add_entry("key1", {"foo": "bar"})
    entry = reg.get_entry("key1")
    assert entry == {"foo": "bar"}

def test_add_entry_duplicate_key():
    """
    Test that adding an entry with a duplicate key raises KeyError.
    """
    reg = Registry()
    reg.add_entry("key1", {"foo": "bar"})
    with pytest.raises(KeyError):
        reg.add_entry("key1", {"baz": "qux"})

def test_update_entry():
    """
    Test updating an existing entry.
    """
    reg = Registry()
    reg.add_entry("key1", {"foo": "bar"})
    reg.update_entry("key1", {"foo": "baz"})
    assert reg.get_entry("key1") == {"foo": "baz"}

def test_update_entry_missing_key():
    """
    Test that updating a non-existent entry raises KeyError.
    """
    reg = Registry()
    with pytest.raises(KeyError):
        reg.update_entry("key1", {"foo": "baz"})

def test_delete_entry():
    """
    Test deleting an entry.
    """
    reg = Registry()
    reg.add_entry("key1", {"foo": "bar"})
    reg.delete_entry("key1")
    assert not reg.is_key_present("key1")

def test_delete_entry_missing_key():
    """
    Test that deleting a non-existent entry raises KeyError.
    """
    reg = Registry()
    with pytest.raises(KeyError):
        reg.delete_entry("key1")

def test_list_keys():
    """
    Test listing all keys in the registry.
    """
    reg = Registry()
    reg.add_entry("key1", {"foo": "bar"})
    reg.add_entry("key2", {"baz": "qux"})
    keys = reg.list_keys()
    assert set(keys) == {"key1", "key2"}

def test_len():
    """
    Test the __len__ method returns the correct number of entries.
    """
    reg = Registry()
    assert len(reg) == 0
    reg.add_entry("key1", {"foo": "bar"})
    assert len(reg) == 1
    reg.add_entry("key2", {"baz": "qux"})
    assert len(reg) == 2
    reg.delete_entry("key1")
    assert len(reg) == 1
