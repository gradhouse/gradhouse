# File: test_patterns.py
# Description: Unit tests for the Patterns class.
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

import pytest
from gradhouse.file.file_type import FileType
from gradhouse.arxiv.patterns import Patterns

@pytest.mark.parametrize(
    "filename,expected",
    [
        ("arXiv_src_9902_005.tar", ("99", "02", "005")),
        ("arXiv_src_2301_001.tar", ("23", "01", "001")),
        ("arXiv_src_2007_123.tar", ("20", "07", "123")),
        ("arXiv_src_0001_000.tar", ("00", "01", "000")),
        ("arXiv_src_9912_999.tar", ("99", "12", "999")),
        # With path
        ("/tmp/arXiv_src_9902_005.tar", ("99", "02", "005")),
        ("./arXiv_src_2301_001.tar", ("23", "01", "001")),
    ]
)
def test_parse_bulk_archive_filename_valid(filename, expected):
    """
    Test the `Patterns.parse_bulk_archive_filename` method with various valid arXiv bulk archive filenames.

    This test uses parameterization to check that the method correctly parses filenames of the form
    'arXiv_src_YYMM_NNN.tar', where:
        - YY: two-digit year
        - MM: two-digit month
        - NNN: three-digit identifier

    The test also covers cases where the filename includes a path.

    Parameters:
        filename (str): The input filename, possibly with a path.
        expected (tuple): The expected tuple of (year, month, identifier) as strings.
    """
    assert Patterns.parse_bulk_archive_filename(filename) == expected

@pytest.mark.parametrize(
    "filename",
    [
        "arXiv_src_9902_05.tar",      # seq_num not 3 digits
        "arXiv_src_9902_005.txt",     # wrong extension
        "arXiv_src_199902_005.tar",   # year not 2 digits
        "arXiv_src_9902.tar",         # missing seq_num
        "arXiv_src_9902_005",         # missing extension
        "src_9902_005.tar",           # missing prefix
        "arXiv_src_9902_005.tgz",     # wrong extension
        "randomfile.tar",             # not matching at all
        "",                           # empty string
        None,                         # NoneType (should raise TypeError)
        # Extra corner cases: extra characters after .tar
        "arXiv_src_9902_005.tar.bak",
        "arXiv_src_9902_005.tar.gz",
        "arXiv_src_9902_005.tarfoo",
        "arXiv_src_9902_005.tar123",
        "arXiv_src_9902_005.tar/",
        "arXiv_src_9902_005.tar.more",
    ]
)
def test_parse_bulk_archive_filename_invalid(filename):
    """
    Unit tests for the `Patterns.parse_bulk_archive_filename` method to ensure it correctly handles
    invalid filename inputs.

    For all invalid string inputs, the method is expected to return `None`.
    For `None` input, the method is expected to raise a `TypeError`.
    """
    if filename is None:
        with pytest.raises(TypeError):
            Patterns.parse_bulk_archive_filename(filename)
    else:
        assert Patterns.parse_bulk_archive_filename(filename) is None

@pytest.mark.parametrize(
    "filename,expected",
    [
        # Valid cases: pattern matches and month is in 01-12
        ("arXiv_src_9902_005.tar", True),
        ("arXiv_src_2301_001.tar", True),
        ("arXiv_src_2007_123.tar", True),
        ("arXiv_src_0001_000.tar", True),
        ("arXiv_src_9912_999.tar", True),
        ("/tmp/arXiv_src_9902_005.tar", True),
        ("./arXiv_src_2301_001.tar", True),
        # Invalid month (00, 13, etc.)
        ("arXiv_src_9913_005.tar", False),
        ("arXiv_src_9900_005.tar", False),
        ("arXiv_src_9915_005.tar", False),
        # Incorrect extension
        ("arXiv_src_9912_005.tar.bak", False),
        ("arXiv_src_9912_005.tar.gz", False),
        ("arXiv_src_9912_005.tarfoo", False),
        ("arXiv_src_9912_005.tar123", False),
        ("arXiv_src_9912_005.tar/", False),
        ("arXiv_src_9912_005.tar.more", False),
        # Completely invalid patterns
        ("arXiv_src_9902_05.tar", False),
        ("arXiv_src_9902_005.txt", False),
        ("arXiv_src_199902_005.tar", False),
        ("arXiv_src_9902.tar", False),
        ("arXiv_src_9902_005", False),
        ("src_9902_005.tar", False),
        ("arXiv_src_9902_005.tgz", False),
        ("randomfile.tar", False),
        ("", False),
    ]
)
def test_is_bulk_archive_filename(filename, expected):
    """
    Unit tests for the `Patterns.is_bulk_archive_filename` method.

    Checks that the method returns True for valid arXiv bulk archive filenames (with valid month)
    and False for invalid patterns or invalid months.
    """
    assert Patterns.is_bulk_archive_filename(filename) == expected

def test_is_bulk_archive_filename_none():
    """
    Test that passing None to is_bulk_archive_filename raises a TypeError.
    """
    with pytest.raises(TypeError):
        Patterns.is_bulk_archive_filename(None)

@pytest.mark.parametrize(
    "filename,expected_uri",
    [
        ("arXiv_src_9902_005.tar", "s3://arxiv/src/arXiv_src_9902_005.tar"),
        ("/tmp/arXiv_src_2301_001.tar", "s3://arxiv/src/arXiv_src_2301_001.tar"),
        ("./arXiv_src_2007_123.tar", "s3://arxiv/src/arXiv_src_2007_123.tar"),
    ]
)
def test_generate_uri_for_bulk_archive_filename_valid(filename, expected_uri):
    """
    Test that generate_uri_for_bulk_archive_filename returns the correct URI for valid filenames.
    """
    assert Patterns.generate_uri_for_bulk_archive_filename(filename) == expected_uri

@pytest.mark.parametrize(
    "filename",
    [
        "arXiv_src_9902_05.tar",      # seq_num not 3 digits
        "arXiv_src_9902_005.txt",     # wrong extension
        "arXiv_src_199902_005.tar",   # year not 2 digits
        "arXiv_src_9902.tar",         # missing seq_num
        "arXiv_src_9902_005",         # missing extension
        "src_9902_005.tar",           # missing prefix
        "arXiv_src_9902_005.tgz",     # wrong extension
        "randomfile.tar",             # not matching at all
        "",                           # empty string
        "arXiv_src_9913_005.tar",     # invalid month
        "arXiv_src_9900_005.tar",     # invalid month
        "arXiv_src_9912_005.tar.bak", # extra after .tar
    ]
)
def test_generate_uri_for_bulk_archive_filename_invalid(filename):
    """
    Test that generate_uri_for_bulk_archive_filename raises ValueError for invalid filenames.
    """
    with pytest.raises(ValueError):
        Patterns.generate_uri_for_bulk_archive_filename(filename)

@pytest.mark.parametrize(
    "filename,expected",
    [
        # Valid old-style filenames
        ("cond-mat9602101.gz", ("cond-mat", "96", "02", "101")),
        ("hep-th9911123.pdf", ("hep-th", "99", "11", "123")),
        ("math0503123.gz", ("math", "05", "03", "123")),
        ("astro-ph0001001.pdf", ("astro-ph", "00", "01", "001")),
        # With path
        ("/tmp/cond-mat9602101.gz", ("cond-mat", "96", "02", "101")),
        ("./hep-th9911123.pdf", ("hep-th", "99", "11", "123")),
    ]
)
def test_parse_old_style_submission_filename_valid(filename, expected):
    """
    Test that the parse_old_style_submission_filename function correctly parses
    old-style arXiv submission filenames that are valid.
    """
    assert Patterns.parse_old_style_submission_filename(filename) == expected

@pytest.mark.parametrize(
    "filename",
    [
        # Invalid extension
        "cond-mat9602101.txt",
        "hep-th9911123.doc",
        # Wrong pattern
        "cond-mat96021.gz",      # number too short
        "cond-mat9602101",       # missing extension
        "cond-mat9602_101.gz",   # underscore instead of direct digits
        "cond-mat9602101.gz.bak",# extra after extension
        "cond-mat9602101gz",     # missing dot before extension
        "cond-mat96021345.gz",   # number too long (could be valid if arXiv allows, but let's test)
        "cond-mat9602.gz",       # missing number
        "cond-mat9602101.",      # empty extension
        "",                      # empty string
        None,                    # NoneType (should raise TypeError)
    ]
)
def test_parse_old_style_submission_filename_invalid(filename):
    """
    Test that the parse_old_style_submission_filename function correctly parses
    old-style arXiv submission filenames that are invalid.
    """    
    if filename is None:
        with pytest.raises(TypeError):
            Patterns.parse_old_style_submission_filename(filename)
    else:
        assert Patterns.parse_old_style_submission_filename(filename) is None

import pytest
from gradhouse.arxiv.patterns import Patterns

@pytest.mark.parametrize(
    "filename,expected",
    [
        # Valid current-style filenames
        ("1202.3054.gz", ("12", "02", "3054")),
        ("9912.12345.pdf", ("99", "12", "12345")),
        ("0001.0001.gz", ("00", "01", "0001")),
        ("2307.54321.pdf", ("23", "07", "54321")),
        # With path
        ("/tmp/1202.3054.gz", ("12", "02", "3054")),
        ("./9912.12345.pdf", ("99", "12", "12345")),
    ]
)
def test_parse_current_style_submission_filename_valid(filename, expected):
    """
    Test that parse_current_style_submission_filename correctly parses valid new-style arXiv submission filenames.

    The method should extract (yy, mm, number) from filenames of the form '{yymm}.{number}.{ext}',
    where ext is '.gz' or '.pdf', and return them as a tuple of strings.
    """
    assert Patterns.parse_current_style_submission_filename(filename) == expected

@pytest.mark.parametrize(
    "filename",
    [
        # Invalid extension
        "1202.3054.txt",
        "9912.12345.doc",
        # Wrong pattern
        "1202-3054.gz",         # dash instead of dot
        "12023054.gz",          # missing dot
        "1202.305.gz",          # number too short
        "1202.305456.gz",       # number too long
        "1202.3054",            # missing extension
        "1202.3054.gz.bak",     # extra after extension
        "1202.3054gz",          # missing dot before extension
        "1202.3054.",           # empty extension
        "",                     # empty string
        None,                   # NoneType (should raise TypeError)
    ]
)
def test_parse_current_style_submission_filename_invalid(filename):
    """
    Test that parse_current_style_submission_filename returns None for invalid new-style arXiv submission filenames.

    The method should return None for filenames with the wrong pattern, wrong extension, or other invalid forms.
    If None is passed as input, a TypeError should be raised.
    """
    if filename is None:
        with pytest.raises(TypeError):
            Patterns.parse_current_style_submission_filename(filename)
    else:
        assert Patterns.parse_current_style_submission_filename(filename) is None

@pytest.mark.parametrize(
    "filename,expected",
    [
        # Valid old-style
        ("cond-mat9602101.gz", True),
        ("hep-th9911123.pdf", True),
        ("math0503123.gz", True),
        ("astro-ph0001001.pdf", True),
        ("/tmp/cond-mat9602101.gz", True),
        ("./hep-th9911123.pdf", True),
        # Valid current-style
        ("1202.3054.gz", True),
        ("9912.12345.pdf", True),
        ("0001.0001.gz", True),
        ("2307.54321.pdf", True),
        ("/tmp/1202.3054.gz", True),
        ("./9912.12345.pdf", True),
        # Invalid old-style
        ("cond-mat9602101.txt", False),
        ("hep-th9911123.doc", False),
        ("cond-mat96021.gz", False),
        ("cond-mat9602101", False),
        ("cond-mat9602_101.gz", False),
        ("cond-mat9602101.gz.bak", False),
        ("cond-mat9602101gz", False),
        ("cond-mat96021345.gz", False),
        ("cond-mat9602.gz", False),
        ("cond-mat9602101.", False),
        # Invalid current-style
        ("1202.3054.txt", False),
        ("9912.12345.doc", False),
        ("1202-3054.gz", False),
        ("12023054.gz", False),
        ("1202.305.gz", False),
        ("1202.305456.gz", False),
        ("1202.3054", False),
        ("1202.3054.gz.bak", False),
        ("1202.3054gz", False),
        ("1202.3054.", False),
        # Completely invalid
        ("", False),
    ]
)
def test_is_submission_filename(filename, expected):
    """
    Test that is_submission_filename returns True for valid old-style and current-style arXiv submission filenames,
    and False for invalid ones.
    """
    assert Patterns.is_submission_filename(filename) == expected

def test_is_submission_filename_none():
    """
    Test that passing None to is_submission_filename raises a TypeError.
    """
    with pytest.raises(TypeError):
        Patterns.is_submission_filename(None)

@pytest.mark.parametrize(
    "filename,expected_url",
    [
        # Old style (category + yymmnnn)
        ("cond-mat9602101.gz", "https://arxiv.org/abs/cond-mat/9602101"),
        ("hep-th9911123.pdf", "https://arxiv.org/abs/hep-th/9911123"),
        ("math0503123.gz", "https://arxiv.org/abs/math/0503123"),
        ("astro-ph0001001.pdf", "https://arxiv.org/abs/astro-ph/0001001"),
        ("/tmp/cond-mat9602101.gz", "https://arxiv.org/abs/cond-mat/9602101"),
        ("./hep-th9911123.pdf", "https://arxiv.org/abs/hep-th/9911123"),
        # New style (yymm.number)
        ("1202.3054.gz", "https://arxiv.org/abs/1202.3054"),
        ("9912.12345.pdf", "https://arxiv.org/abs/9912.12345"),
        ("0001.0001.gz", "https://arxiv.org/abs/0001.0001"),
        ("2307.54321.pdf", "https://arxiv.org/abs/2307.54321"),
        ("/tmp/1202.3054.gz", "https://arxiv.org/abs/1202.3054"),
        ("./9912.12345.pdf", "https://arxiv.org/abs/9912.12345"),
    ]
)
def test_generate_url_for_submission_filename_valid(filename, expected_url):
    """
    Test that generate_url_for_submission_filename returns the correct arXiv URL
    for valid old-style and new-style submission filenames.
    """
    assert Patterns.generate_url_for_submission_filename(filename) == expected_url

@pytest.mark.parametrize(
    "filename",
    [
        # Invalid old style
        "cond-mat9602101.txt",
        "hep-th9911123.doc",
        "cond-mat96021.gz",
        "cond-mat9602101",
        "cond-mat9602_101.gz",
        "cond-mat9602101.gz.bak",
        "cond-mat9602101gz",
        "cond-mat96021345.gz",
        "cond-mat9602.gz",
        "cond-mat9602101.",
        # Invalid new style
        "1202.3054.txt",
        "9912.12345.doc",
        "1202-3054.gz",
        "12023054.gz",
        "1202.305.gz",
        "1202.305456.gz",
        "1202.3054",
        "1202.3054.gz.bak",
        "1202.3054gz",
        "1202.3054.",
        # Completely invalid
        "",
        None,
    ]
)
def test_generate_url_for_submission_filename_invalid(filename):
    """
    Test that generate_url_for_submission_filename raises ValueError for invalid
    old-style and new-style submission filenames.
    """
    if filename is None:
        with pytest.raises(TypeError):
            Patterns.generate_url_for_submission_filename(filename)
    else:
        with pytest.raises(ValueError):
            Patterns.generate_url_for_submission_filename(filename)

@pytest.mark.parametrize(
    "file_path,expected_errors,expected_valid",
    [
        # Invalid filename pattern
        ("not_a_bulk_archive.tar", ["Filename not_a_bulk_archive.tar does not match bulk archive pattern"], False),
        # File does not exist (but pattern is valid)
        ("arXiv_src_9902_005.tar", ["File arXiv_src_9902_005.tar not found"], False),
        # Invalid extension (simulate file exists)
        ("arXiv_src_9902_005.txt", ["Filename arXiv_src_9902_005.txt does not match bulk archive pattern"], False),
        # Valid file, but extension/type/format errors (simulate with mocks)
        # These cases require monkeypatching/mocking if you want to simulate file existence and type checks.
    ]
)
def test_check_bulk_archive_and_is_bulk_archive_valid_basic(file_path, expected_errors, expected_valid, mocker):
    """
    Test check_bulk_archive and is_bulk_archive_valid for basic error cases.
    """
    # Mock os.path.isfile to simulate file existence for the second case
    if file_path == "arXiv_src_9902_005.tar":
        mocker.patch("os.path.isfile", return_value=False)
    else:
        mocker.patch("os.path.isfile", return_value=True)

    # Mock FileHandler methods to avoid dependency on actual files
    mocker.patch("gradhouse.file.file_handler.FileHandler.get_file_type_from_extension",
                 return_value=[FileType.FILE_TYPE_ARCHIVE_TAR])
    mocker.patch("gradhouse.file.file_handler.FileHandler.get_file_type_from_format",
                 return_value=FileType.FILE_TYPE_ARCHIVE_TAR)
    mocker.patch("gradhouse.file.handler.archive_handler.ArchiveHandler.check_extract_possible", return_value=[])
    mocker.patch("gradhouse.file.handler.archive_handler.ArchiveHandler.list_contents", return_value=["1202.3054.gz"])

    errors = Patterns.check_bulk_archive(file_path)
    assert errors == expected_errors
    assert Patterns.is_bulk_archive_valid(file_path) == expected_valid

def test_check_bulk_archive_and_is_bulk_archive_valid_success(mocker):
    """
    Test check_bulk_archive and is_bulk_archive_valid for a fully valid bulk archive file.
    """
    file_path = "arXiv_src_9902_005.tar"
    mocker.patch("os.path.isfile", return_value=True)
    mocker.patch("gradhouse.file.file_handler.FileHandler.get_file_type_from_extension",
                 return_value=[FileType.FILE_TYPE_ARCHIVE_TAR])
    mocker.patch("gradhouse.file.file_handler.FileHandler.get_file_type_from_format",
                 return_value=FileType.FILE_TYPE_ARCHIVE_TAR)
    mocker.patch("gradhouse.file.handler.archive_handler.ArchiveHandler.check_extract_possible", return_value=[])
    mocker.patch("gradhouse.file.handler.archive_handler.ArchiveHandler.list_contents", return_value=["1202.3054.gz"])

    errors = Patterns.check_bulk_archive(file_path)
    assert errors == []
    assert Patterns.is_bulk_archive_valid(file_path) is True

def test_check_bulk_archive_invalid_archive_contents(mocker):
    """
    Test check_bulk_archive for a valid archive file with invalid contents.
    """
    file_path = "arXiv_src_9902_005.tar"
    mocker.patch("os.path.isfile", return_value=True)
    mocker.patch("gradhouse.file.file_handler.FileHandler.get_file_type_from_extension",
                 return_value=[FileType.FILE_TYPE_ARCHIVE_TAR])
    mocker.patch("gradhouse.file.file_handler.FileHandler.get_file_type_from_format",
                 return_value=FileType.FILE_TYPE_ARCHIVE_TAR)
    mocker.patch("gradhouse.file.handler.archive_handler.ArchiveHandler.check_extract_possible", return_value=[])
    # Simulate invalid archive contents
    mocker.patch("gradhouse.file.handler.archive_handler.ArchiveHandler.list_contents", return_value=["not_a_submission.txt", "1202.3054.gz"])

    errors = Patterns.check_bulk_archive(file_path)
    assert errors == ["Archive entries do not match submission filename pattern: not_a_submission.txt"]
    assert Patterns.is_bulk_archive_valid(file_path) is False

def test_check_bulk_archive_extension_not_tar(mocker):
    """
    Test check_bulk_archive when the file extension is not recognized as tar.
    """
    file_path = "arXiv_src_9902_005.tar"
    mocker.patch("os.path.isfile", return_value=True)
    # Simulate extension is not tar
    mocker.patch("gradhouse.file.file_handler.FileHandler.get_file_type_from_extension", return_value=[])
    mocker.patch("gradhouse.file.file_handler.FileHandler.get_file_type_from_format", return_value=FileType.FILE_TYPE_ARCHIVE_TAR)
    mocker.patch("gradhouse.file.handler.archive_handler.ArchiveHandler.check_extract_possible", return_value=[])
    mocker.patch("gradhouse.file.handler.archive_handler.ArchiveHandler.list_contents", return_value=["1202.3054.gz"])

    errors = Patterns.check_bulk_archive(file_path)
    assert errors == ['File extension is not tar']
    assert Patterns.is_bulk_archive_valid(file_path) is False

def test_check_bulk_archive_format_not_tar(mocker):
    """
    Test check_bulk_archive when the file format is not tar, even though the extension is correct.
    """
    file_path = "arXiv_src_9902_005.tar"
    mocker.patch("os.path.isfile", return_value=True)
    # Simulate extension is tar, but format is not tar
    mocker.patch("gradhouse.file.file_handler.FileHandler.get_file_type_from_extension", return_value=[FileType.FILE_TYPE_ARCHIVE_TAR])
    mocker.patch("gradhouse.file.file_handler.FileHandler.get_file_type_from_format", return_value="not_tar")
    mocker.patch("gradhouse.file.handler.archive_handler.ArchiveHandler.check_extract_possible", return_value=[])
    mocker.patch("gradhouse.file.handler.archive_handler.ArchiveHandler.list_contents", return_value=["1202.3054.gz"])

    errors = Patterns.check_bulk_archive(file_path)
    assert errors == ['File format is not tar']
    assert Patterns.is_bulk_archive_valid(file_path) is False

@pytest.mark.parametrize(
    "file_path,pattern_valid,file_exists,ext_types,format_type,archive_errors,expected_errors,expected_valid",
    [
        # Invalid filename pattern
        ("not_a_submission.pdf", False, True, [FileType.FILE_TYPE_PDF], FileType.FILE_TYPE_PDF, [], ["Filename not_a_submission.pdf does not match submission pattern"], False),
        # File does not exist
        ("1202.3051.pdf", True, False, [FileType.FILE_TYPE_PDF], FileType.FILE_TYPE_PDF, [], ["File 1202.3051.pdf not found"], False),
        # Extension not allowed
        ("1202.3052.txt", True, True, [], FileType.FILE_TYPE_PDF, [], ["File extension type is not allowed"], False),
        # Format not allowed
        ("1202.3053.pdf", True, True, [FileType.FILE_TYPE_PDF], FileType.FILE_TYPE_XML, [], ["File type XML not allowed"], False),
        # Format does not match extension
        ("1202.3054.pdf", True, True, [FileType.FILE_TYPE_PDF], FileType.FILE_TYPE_ARCHIVE_GZ, [], ["File format does not match file extension"], False),
        # Archive extraction errors
        ("1202.3055.gz", True, True, [FileType.FILE_TYPE_ARCHIVE_GZ], FileType.FILE_TYPE_ARCHIVE_GZ, ["archive error"], ["archive error"], False),
        # All valid (PDF)
        ("1202.3056.pdf", True, True, [FileType.FILE_TYPE_PDF], FileType.FILE_TYPE_PDF, [], [], True),
        # All valid (GZ)
        ("1202.3057.gz", True, True, [FileType.FILE_TYPE_ARCHIVE_GZ], FileType.FILE_TYPE_ARCHIVE_GZ, [], [], True),
    ]
)
def test_check_submission_and_is_submission_valid(
    mocker, file_path, pattern_valid, file_exists, ext_types, format_type, archive_errors, expected_errors, expected_valid
):
    """
    Test check_submission and is_submission_valid for various scenarios.
    """
    # Mock Patterns.is_submission_filename
    mocker.patch("gradhouse.arxiv.patterns.Patterns.is_submission_filename", return_value=pattern_valid)
    # Mock os.path.isfile
    mocker.patch("os.path.isfile", return_value=file_exists)
    # Mock FileHandler.get_file_type_from_extension
    mocker.patch("gradhouse.file.file_handler.FileHandler.get_file_type_from_extension", return_value=ext_types)
    # Mock FileHandler.get_file_type_from_format
    mocker.patch("gradhouse.file.file_handler.FileHandler.get_file_type_from_format", return_value=format_type)
    # Mock ArchiveHandler.check_extract_possible
    mocker.patch("gradhouse.file.handler.archive_handler.ArchiveHandler.check_extract_possible", return_value=archive_errors)

    errors = Patterns.check_submission(file_path)
    assert errors == expected_errors
    assert Patterns.is_submission_valid(file_path) == expected_valid

def test_check_submission_archive_extraction_only_if_archive(mocker):
    """
    Test that archive extraction errors are only checked for allowed archive types.
    """
    file_path = "1202.3054.pdf"
    mocker.patch("gradhouse.arxiv.patterns.Patterns.is_submission_filename", return_value=True)
    mocker.patch("os.path.isfile", return_value=True)
    mocker.patch("gradhouse.file.file_handler.FileHandler.get_file_type_from_extension", return_value=[FileType.FILE_TYPE_PDF])
    mocker.patch("gradhouse.file.file_handler.FileHandler.get_file_type_from_format", return_value=FileType.FILE_TYPE_PDF)
    # Should not call check_extract_possible for PDF
    mock_check_extract = mocker.patch("gradhouse.file.handler.archive_handler.ArchiveHandler.check_extract_possible", return_value=["archive error"])

    errors = Patterns.check_submission(file_path)
    assert errors == []
    assert Patterns.is_submission_valid(file_path) is True
    mock_check_extract.assert_not_called()