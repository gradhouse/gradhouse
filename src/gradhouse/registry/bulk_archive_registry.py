# File: bulk_archive_registry.py
# Description: Manages the registration and tracking of bulk archive files within the application
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

class BulkArchiveRegistry(Registry):
    """
    This module provides the BulkArchiveRegistry class, which manages the registration and tracking of bulk archive
    files, such as those downloaded from arXiv or similar repositories. It offers methods for adding, removing,
    and querying archive entries, supporting efficient management of large collections of archive data.

    The key for each entry is the SHA256 hash of the bulk archive file with the entry comprised as a dictionary
    with the metadata and bulk archive origin.

    The BulkArchiveRegistry does not contain the SHA256 hashes for each Submission entry of the tar
    """

    pass
