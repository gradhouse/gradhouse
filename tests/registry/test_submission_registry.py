# File: test_submission_registry.py
# Description: Unit tests for the SubmissionRegistry class.
#
# Copyright (c) 2025 Jason Stuber
# Licensed under the MIT License. See the LICENSE file for more details.

from gradhouse.registry.submission_registry import SubmissionRegistry
from gradhouse.registry.registry import Registry

# Unit tests are already in place for the Registry class.
# Only those tests specific to the SubmissionRegistry class will be added here.

def test_submission_registry_initialization():
    """
    Test that SubmissionRegistry initializes correctly and is an instance of Registry.
    """
    reg = SubmissionRegistry()
    assert isinstance(reg, SubmissionRegistry)
    assert isinstance(reg, Registry)
    assert hasattr(reg, "_registry")
    assert reg._registry == {}
