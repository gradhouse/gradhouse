# File: test_tex_handler.py
# Description: Unit tests for the TexHandler class.
#
# Copyright (c) 2025 Jason Stuber
# Licensed under the MIT License. See the LICENSE file for more details.

import os
import pytest

from gradhouse.file.handler.tex_handler import TexHandler
from gradhouse.file.file_type import FileType


# test data directory
TEST_DIRECTORY = os.path.dirname(os.path.dirname(__file__))
TEST_DATA_DIRECTORY = os.path.join(TEST_DIRECTORY, 'sample_files')

@pytest.mark.parametrize("file_extension, expected_type", [
    ('.aux', [FileType.FILE_TYPE_TEX_AUX]),
    ('.bbl', [FileType.FILE_TYPE_TEX_BBL]),
    ('.bib', [FileType.FILE_TYPE_TEX_BIB]),
    ('.bst', [FileType.FILE_TYPE_TEX_BST]),
    ('.clo', [FileType.FILE_TYPE_TEX_CLO]),
    ('.cls', [FileType.FILE_TYPE_TEX_CLS]),
    ('.dvi', [FileType.FILE_TYPE_TEX_DVI]),
    ('.fig', [FileType.FILE_TYPE_TEX_FIG]),
    ('.log', [FileType.FILE_TYPE_TEX_LOG]),
    ('.pstex', [FileType.FILE_TYPE_TEX_PSTEX]),
    ('.pstex_t', [FileType.FILE_TYPE_TEX_PSTEX_T]),
    ('.sty', [FileType.FILE_TYPE_TEX_STY]),
    ('.synctex', [FileType.FILE_TYPE_TEX_SYNCTEX]),
    ('.tex', [FileType.FILE_TYPE_TEX_TEX,
              FileType.FILE_TYPE_TEX_LATEX_209_MAIN,
              FileType.FILE_TYPE_TEX_LATEX_2E_MAIN]),
    ('.tikz', [FileType.FILE_TYPE_TEX_TIKZ]),
    ('.toc', [FileType.FILE_TYPE_TEX_TOC]),
    ('.tex2', [FileType.FILE_TYPE_UNKNOWN]),
    ('', [FileType.FILE_TYPE_UNKNOWN])
])
def test_get_file_type_from_extension(file_extension, expected_type):
    """
    Test the get_file_type_from_extension function
    """
    file_type = TexHandler.get_file_type_from_extension(file_extension)
    assert file_type == expected_type

@pytest.mark.parametrize("filename, expected_file_type", [
    ('tex/latex2e_example.tex', FileType.FILE_TYPE_TEX_LATEX_2E_MAIN),
    ('tex/latex209_example.tex', FileType.FILE_TYPE_TEX_LATEX_209_MAIN),
    ('tex/latex2e_example_non_utf8.tex', FileType.FILE_TYPE_UNKNOWN),
    ('ps/eps_file.eps', FileType.FILE_TYPE_UNKNOWN)
])
def test_get_file_type_from_format(filename, expected_file_type):
    """
    Test the get_file_type_from_format method when the file is present.
    """
    full_path = os.path.join(TEST_DATA_DIRECTORY, filename)
    file_type = TexHandler.get_file_type_from_format(full_path)
    assert file_type == expected_file_type

def test_get_file_type_from_format_raise_file_not_found():
    """
    Test the get_file_type_from_format method when the file is not found or the path directs to a non-file
    """
    # Test case: directory, is_postscript is only for files
    file_path = TEST_DATA_DIRECTORY
    with pytest.raises(FileNotFoundError):
        TexHandler.get_file_type_from_format(file_path)

    # Test case: file not found
    file_path = 'this_is_not_a_file'
    with pytest.raises(FileNotFoundError):
        TexHandler.get_file_type_from_format(file_path)

def test_get_file_extension_map():
    """
    Test that get_file_extension_map returns the correct file extension map.
    """
    expected_map = {
        '.aux': [FileType.FILE_TYPE_TEX_AUX],
        '.bbl': [FileType.FILE_TYPE_TEX_BBL],
        '.bib': [FileType.FILE_TYPE_TEX_BIB],
        '.bst': [FileType.FILE_TYPE_TEX_BST],
        '.clo': [FileType.FILE_TYPE_TEX_CLO],
        '.cls': [FileType.FILE_TYPE_TEX_CLS],
        '.dvi': [FileType.FILE_TYPE_TEX_DVI],
        '.fig': [FileType.FILE_TYPE_TEX_FIG],
        '.log': [FileType.FILE_TYPE_TEX_LOG],
        '.pstex': [FileType.FILE_TYPE_TEX_PSTEX],
        '.pstex_t': [FileType.FILE_TYPE_TEX_PSTEX_T],
        '.sty': [FileType.FILE_TYPE_TEX_STY],
        '.synctex': [FileType.FILE_TYPE_TEX_SYNCTEX],
        '.tex': [FileType.FILE_TYPE_TEX_TEX,
                 FileType.FILE_TYPE_TEX_LATEX_209_MAIN,
                 FileType.FILE_TYPE_TEX_LATEX_2E_MAIN],
        '.tikz': [FileType.FILE_TYPE_TEX_TIKZ],
        '.toc': [FileType.FILE_TYPE_TEX_TOC]
    }

    result = TexHandler.get_file_extension_map()

    assert isinstance(result, dict), "The result should be a dictionary."
    assert result == expected_map, "The returned file extension map is incorrect."
