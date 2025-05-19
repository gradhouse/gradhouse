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

class BulkArchiveRegistry:
    """
    This module provides the BulkArchiveRegistry class, which manages the registration and tracking of bulk archive
    files, such as those downloaded from arXiv or similar repositories. It offers methods for adding, removing,
    and querying archive entries, supporting efficient management of large collections of archive data.
    """

    def __init__(self) -> None:
        """
        Initializes a new instance of the BulkArchiveRegistry class.

        This constructor sets up the internal _registry dictionary for the bulk archive files, each bulk archive file
        being a .tar file comprised of multiple submissions.

        The key for each entry is the SHA256 hash of the bulk archive file with the entry comprised as a dictionary
        with the metadata and bulk archive origin.

        Submission contents and submission hashes are not contained in this registry.
        """

        self._registry = dict()

    def clear(self) -> None:
        """
        Clears the registry and resets it to its default state.
        """

        self._registry.clear()
