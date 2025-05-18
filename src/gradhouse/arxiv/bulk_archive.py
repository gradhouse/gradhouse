# File: bulk_archive.py
# Description: Bulk source archive downloaded from the arXiv S3 service.
#
# Copyright (c) 2025 Jason Stuber
# Licensed under the MIT License. See the LICENSE file for more details.
#
# Disclaimer:
# This project is not affiliated with, endorsed by, or sponsored by arXiv or Cornell University.
# arXiv® is a registered trademark of Cornell University.
# All arXiv data and trademarks are the property of their respective owners.
# For more information, see https://arxiv.org/help/license and https://info.arxiv.org/help/bulk_data_s3.html


class BulkArchive:
    """
    This class provides functions to handle the bulk source archive files arXiv_src_yymm_seq.tar that can be
    downloaded from the arXiv S3 service. Each bulk archive contains the source packages for multiple arXiV
    submissions. Each submission within the archive typically includes LaTeX files, figures, and other resources
    needed to compile the paper.

    Each bulk source archive corresponds to a single entry in the arXiV_src_manifest.xml manifest.

    For more details about arXiv and bulk data downloads, please refer to the following resources:
        https://www.arxiv.org
        https://info.arxiv.org/help/bulk_data_s3.html

    """

    def __init__(self) -> None:
        """
        Initializes a new instance of the BulkArchive class.
        """

        self._bulk_archive = dict()

    def clear(self) -> None:
        """
        Clears the bulk archive and resets it to its default state.
        """

        self._bulk_archive.clear()
