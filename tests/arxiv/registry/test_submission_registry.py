# File: test_submission_registry.py
# Description: Unit tests for the SubmissionRegistry class.
#
# Copyright (c) 2025 Jason Stuber
# Licensed under the MIT License. See the LICENSE file for more details.
#
# Disclaimer:
# This software is not affiliated with, endorsed by, or sponsored by arXiv, Cornell University, or any of their affiliates.
# All arXiv data, logos, and trademarks are the property of their respective owners.
# Users of this software are solely responsible for ensuring their use of arXiv data complies with arXiv's policies and terms.
# For more information, see:
# - https://arxiv.org/help/license
# - https://info.arxiv.org/help/bulk_data_s3.html

from gradhouse.arxiv.registry.submission_registry import SubmissionRegistry

def test_submission_registry_initialization():
    """
    Test that SubmissionRegistry initializes with an empty _registry dictionary.
    """
    archive = SubmissionRegistry()
    assert isinstance(archive._registry, dict)
    assert archive._registry == {}

def test_submission_registry_clear():
    """
    Test that SubmissionRegistry.clear() empties the _registry dictionary.
    """
    archive = SubmissionRegistry()
    archive._registry['test'] = 'value'
    assert archive._registry != {}
    archive.clear()
    assert archive._registry == {}
