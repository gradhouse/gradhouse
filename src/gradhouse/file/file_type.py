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

    FILE_TYPE_IMAGE_BMP = 'IMAGE_BMP'
    FILE_TYPE_IMAGE_GIF = 'IMAGE_GIF'
    FILE_TYPE_IMAGE_ICO = 'IMAGE_ICO'
    FILE_TYPE_IMAGE_JPG = 'IMAGE_JPG'
    FILE_TYPE_IMAGE_PNG = 'IMAGE_PNG'
    FILE_TYPE_IMAGE_SVG = 'IMAGE_SVG'
    FILE_TYPE_IMAGE_TIFF = 'IMAGE_TIFF'

    FILE_TYPE_PDF = 'PDF'

    FILE_TYPE_POSTSCRIPT_PS = 'POSTSCRIPT_PS'
    FILE_TYPE_POSTSCRIPT_EPS = 'POSTSCRIPT_EPS'
    FILE_TYPE_POSTSCRIPT_EPSF = 'POSTSCRIPT_EPSF'
    FILE_TYPE_POSTSCRIPT_EPSI = 'POSTSCRIPT_EPSI'

    FILE_TYPE_XML = 'XML'

    FILE_TYPE_TEX_AUX = 'TEX_AUX'
    FILE_TYPE_TEX_BBL = 'TEX_BBL'
    FILE_TYPE_TEX_BIB = 'TEX_BIB'
    FILE_TYPE_TEX_BST = 'TEX_BST'
    FILE_TYPE_TEX_CLO = 'TEX_CLO'                       # class options
    FILE_TYPE_TEX_CLS = 'TEX_CLS'
    FILE_TYPE_TEX_DVI = 'TEX_DVI'
    FILE_TYPE_TEX_FIG = 'TEX_FIG'                       # xfig
    FILE_TYPE_TEX_LOG = 'TEX_LOG'
    FILE_TYPE_TEX_PSTEX = 'TEX_PSTEX'                   # ps part of xfig export
    FILE_TYPE_TEX_PSTEX_T = 'TEX_PSTEX_T'               # LaTeX part of xfig export
    FILE_TYPE_TEX_STY = 'TEX_STY'
    FILE_TYPE_TEX_SYNCTEX = 'TEX_SYNCTEX'               # used for sync tools between latex file and pdf
    FILE_TYPE_TEX_TEX = 'TEX_TEX'
    FILE_TYPE_TEX_LATEX_209_MAIN = 'TEX_LATEX_209_MAIN' # LaTeX 2.09 main file
    FILE_TYPE_TEX_LATEX_2E_MAIN = 'TEX_LATEX_2E_MAIN'   # LaTeX 2e main file
    FILE_TYPE_TEX_TIKZ = 'TEX_TIKZ'                     # TikZ ist kein Zeichenprogramm package
    FILE_TYPE_TEX_TOC = 'TEX_TOC'
