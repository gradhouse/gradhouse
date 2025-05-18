# File: submission_parser.py
# Description: Parse an arXiv submission
#
# Copyright (c) 2025 Jason Stuber
# Licensed under the MIT License. See the LICENSE file for more details.
#
# Disclaimer:
# This project is not affiliated with, endorsed by, or sponsored by arXiv or Cornell University.
# arXiv® is a registered trademark of Cornell University.
# All arXiv data and trademarks are the property of their respective owners.
# For more information, see https://arxiv.org/help/license and https://info.arxiv.org/help/bulk_data_s3.html


import os
import re

class SubmissionParser:
    """
    Submission parser for arXiv submission source files.
    """

    @staticmethod
    def get_arxiv_url_from_filename(filename: str) -> str:
        """
        Given the arXiv submission filename return the URL.

        Submission filenames have one of the two patterns:
            1. Subject and number: this is the older classification scheme.
            The filename 9602/cond-mat9602101.gz resolves to the arXiv URL https://arxiv.org/abs/cond-mat/9602101
            2. Number only: this is the newest classification scheme.
            The filename 1202/1202.3054.gz resolves to the arXiv URL https://arxiv.org/abs/1202.3054

        :param filename: str, file name. This function strips the directory.
        :return: str, arXiv URL to the arXiv submission. This has the prefix https://arxiv.org/abs/
        """

        base_url = 'https://arxiv.org/abs/'
        basename = os.path.basename(filename)
        basename_no_ext = os.path.splitext(basename)[0]

        # Check if the filename starts with a category (e.g., astro-ph)
        match = re.match(r'^([a-z\-]+)(\d+)$', basename_no_ext)
        if match:
            category, number = match.groups()
            # Insert a slash before the number part
            arxiv_url = f"{base_url}{category}/{number}"
        else:
            # Modern arXiv IDs (e.g., 2302.00382)
            arxiv_url = f"{base_url}{basename_no_ext}"

        return arxiv_url
