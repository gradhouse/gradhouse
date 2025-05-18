# File: test_submission_parser.py
# Description: Unit tests for the SubmissionParser class.
#
# Copyright (c) 2025 Jason Stuber
# Licensed under the MIT License. See the LICENSE file for more details.
#
# Disclaimer:
# This project is not affiliated with, endorsed by, or sponsored by arXiv or Cornell University.
# arXiv® is a registered trademark of Cornell University.
# All arXiv data and trademarks are the property of their respective owners.
# For more information, see https://arxiv.org/help/license and https://info.arxiv.org/help/bulk_data_s3.html

import pytest
from gradhouse.arxiv.submission_parser import SubmissionParser

@pytest.mark.parametrize("filename,expected_url", [
    # Old-style arXiv ID with category
    ("astro-ph0302001.gz", "https://arxiv.org/abs/astro-ph/0302001"),
    ("cond-mat9602101.gz", "https://arxiv.org/abs/cond-mat/9602101"),
    # New-style arXiv ID
    ("2302.00382.gz", "https://arxiv.org/abs/2302.00382"),
    ("1202.3054.gz", "https://arxiv.org/abs/1202.3054"),
    # With directory in path
    ("9602/cond-mat9602101.gz", "https://arxiv.org/abs/cond-mat/9602101"),
    ("1202/1202.3054.gz", "https://arxiv.org/abs/1202.3054"),
    # Edge cases
    ("math0506203.gz", "https://arxiv.org/abs/math/0506203"),
    ("hep-th9901001.gz", "https://arxiv.org/abs/hep-th/9901001"),
])
def test_get_arxiv_url_from_filename(filename, expected_url):
    assert SubmissionParser.get_arxiv_url_from_filename(filename) == expected_url
