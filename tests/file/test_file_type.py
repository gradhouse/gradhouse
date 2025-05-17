# File: test_file_type.py
# Description: Unit tests for the FileType class.
#
# Copyright (c) 2025 Jason Stuber
# Licensed under the MIT License. See the LICENSE file for more details.

from gradhouse.file.file_type import FileType


def test_enum_members_exist():
    """
    Test that the FileType members are present
    """
    assert hasattr(FileType, 'FILE_TYPE_UNKNOWN')

    assert hasattr(FileType, 'FILE_TYPE_ARCHIVE_GZ')
    assert hasattr(FileType, 'FILE_TYPE_ARCHIVE_TAR')
    assert hasattr(FileType, 'FILE_TYPE_ARCHIVE_TGZ')


    assert hasattr(FileType, 'FILE_TYPE_PDF')
    assert hasattr(FileType, 'FILE_TYPE_POSTSCRIPT_PS')
    assert hasattr(FileType, 'FILE_TYPE_POSTSCRIPT_EPS')
    assert hasattr(FileType, 'FILE_TYPE_POSTSCRIPT_EPSF')
    assert hasattr(FileType, 'FILE_TYPE_POSTSCRIPT_EPSI')
    assert hasattr(FileType, 'FILE_TYPE_XML')

def test_enum_values():
    """
    Test that the FileType enum values match expected values
    """
    assert FileType.FILE_TYPE_UNKNOWN.value == 'UNKNOWN'

    assert FileType.FILE_TYPE_ARCHIVE_GZ.value == 'ARCHIVE_GZ'
    assert FileType.FILE_TYPE_ARCHIVE_TAR.value == 'ARCHIVE_TAR'
    assert FileType.FILE_TYPE_ARCHIVE_TGZ.value == 'ARCHIVE_TGZ'

    assert FileType.FILE_TYPE_PDF.value == 'PDF'
    assert FileType.FILE_TYPE_POSTSCRIPT_PS.value == 'POSTSCRIPT_PS'
    assert FileType.FILE_TYPE_POSTSCRIPT_EPS.value == 'POSTSCRIPT_EPS'
    assert FileType.FILE_TYPE_POSTSCRIPT_EPSF.value == 'POSTSCRIPT_EPSF'
    assert FileType.FILE_TYPE_POSTSCRIPT_EPSI.value == 'POSTSCRIPT_EPSI'
    assert FileType.FILE_TYPE_XML.value == 'XML'

def test_enum_no_extra_members():
    """
    Test that no new members have been added to the FileType enum.
    """

    expected_members = {'FILE_TYPE_UNKNOWN',
                        'FILE_TYPE_ARCHIVE_GZ', 'FILE_TYPE_ARCHIVE_TAR', 'FILE_TYPE_ARCHIVE_TGZ',
                        'FILE_TYPE_PDF',
                        'FILE_TYPE_POSTSCRIPT_PS', 'FILE_TYPE_POSTSCRIPT_EPS',
                        'FILE_TYPE_POSTSCRIPT_EPSF', 'FILE_TYPE_POSTSCRIPT_EPSI',
                        'FILE_TYPE_XML'}
    actual_members = set(FileType.__members__.keys())
    assert actual_members == expected_members, f"Unexpected members found: {actual_members - expected_members}"
