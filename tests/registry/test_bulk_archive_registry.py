# File: test_bulk_archive_registry.py
# Description: Unit tests for the BulkArchiveRegistry class.
#
# Copyright (c) 2025 Jason Stuber
# Licensed under the MIT License. See the LICENSE file for more details.


from gradhouse.registry.bulk_archive_registry import BulkArchiveRegistry
from gradhouse.registry.registry import Registry

# Unit tests are already in place for the Registry class.
# Only those tests specific to the BulkArchiveRegistry class will be added here.

def test_bulk_archive_registry_initialization():
    """
    Test that BulkArchiveRegistry initializes correctly and is an instance of Registry.
    """
    reg = BulkArchiveRegistry()
    assert isinstance(reg, BulkArchiveRegistry)
    assert isinstance(reg, Registry)
    assert hasattr(reg, "_registry")
    assert reg._registry == {}
