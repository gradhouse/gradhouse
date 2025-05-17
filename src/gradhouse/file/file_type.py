# File: file_type.py
# Description: File type categories.
#
# Copyright (c) 2025 Jason Stuber
# Licensed under the MIT License. See the LICENSE file for more details.


from enum import Enum

class FileType(Enum):
    """
    Enumeration for file type categories.

    This enum is used to categorize files based on their extension or format.
    """

    FILE_TYPE_UNKNOWN = 'UNKNOWN'

    FILE_TYPE_ARCHIVE_GZ = 'ARCHIVE_GZ'
    FILE_TYPE_ARCHIVE_TAR = 'ARCHIVE_TAR'
    FILE_TYPE_ARCHIVE_TGZ = 'ARCHIVE_TGZ'

    FILE_TYPE_PDF = 'PDF'

    FILE_TYPE_POSTSCRIPT_PS = 'POSTSCRIPT_PS'
    FILE_TYPE_POSTSCRIPT_EPS = 'POSTSCRIPT_EPS'
    FILE_TYPE_POSTSCRIPT_EPSF = 'POSTSCRIPT_EPSF'
    FILE_TYPE_POSTSCRIPT_EPSI = 'POSTSCRIPT_EPSI'

    FILE_TYPE_XML = 'XML'
