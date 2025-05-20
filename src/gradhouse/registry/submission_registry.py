# File: submission_registry.py
# Description: Maintains a registry of individual submissions identified by unique keys
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

from .registry import Registry

class SubmissionRegistry(Registry):
    """
    This module defines the SubmissionRegistry class, responsible for maintaining a registry of individual submissions
    or entries, typically identified by unique hash keys. It provides methods to add, check, delete, and clear
    submission records, facilitating organized tracking of submission data within the application.

    The key for each entry is the SHA256 hash of the submission file with the value as a dictionary with the
    metadata and submission origin.

    The submission contents are not contained in this registry.
    """

    pass
