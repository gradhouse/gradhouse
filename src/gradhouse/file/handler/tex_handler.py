# File: tex_handler.py
# Description: TeX and LaTeX file handler methods
#
# Copyright (c) 2025 Jason Stuber
# Licensed under the MIT License. See the LICENSE file for more details.

import os

from gradhouse.file.file_system import FileSystem
from gradhouse.file.file_type import FileType

class TexHandler:
    """
    A class to handle TeX and LaTeX files.
    """

    _file_extension_map = {
        '.aux': [FileType.FILE_TYPE_TEX_AUX],
        '.bbl': [FileType.FILE_TYPE_TEX_BBL],
        '.bib': [FileType.FILE_TYPE_TEX_BIB],
        '.bst': [FileType.FILE_TYPE_TEX_BST],
        '.clo': [FileType.FILE_TYPE_TEX_CLO],
        '.cls' : [FileType.FILE_TYPE_TEX_CLS],
        '.dvi': [FileType.FILE_TYPE_TEX_DVI],
        '.fig': [FileType.FILE_TYPE_TEX_FIG],
        '.log': [FileType.FILE_TYPE_TEX_LOG],
        '.pstex': [FileType.FILE_TYPE_TEX_PSTEX],
        '.pstex_t': [FileType.FILE_TYPE_TEX_PSTEX_T],
        '.sty' : [FileType.FILE_TYPE_TEX_STY],
        '.synctex': [FileType.FILE_TYPE_TEX_SYNCTEX],
        '.tex' : [FileType.FILE_TYPE_TEX_TEX,
                  FileType.FILE_TYPE_TEX_LATEX_209_MAIN,
                  FileType.FILE_TYPE_TEX_LATEX_2E_MAIN],
        '.tikz' : [FileType.FILE_TYPE_TEX_TIKZ],
        '.toc': [FileType.FILE_TYPE_TEX_TOC]
    }

    @staticmethod
    def get_file_extension_map() -> dict:
        """
        Get the file extension map.
        :return: dict, dictionary of file extension and a list of associated file types.
        """

        return TexHandler._file_extension_map

    @staticmethod
    def get_file_type_from_extension(file_extension: str) -> list:
        """
        Determine the file type from the file extension.

        :param file_extension: str, file extension
        :return: list, list of file type categories FileType determined by extension.
            If the file type is unknown, return FILE_TYPE_UNKNOWN.
        """

        return TexHandler._file_extension_map.get(file_extension.lower(), [FileType.FILE_TYPE_UNKNOWN])

    @staticmethod
    def is_utf8_encoded(file_path: str) -> bool:
        """
        Determine if the file is UTF-8 encoded.

        :param file_path: str, path to the file
        :return: bool, True if the file is UTF-8 encoded, otherwise False

        :raises FileNotFoundError: If the file is not found.
        """

        is_file_found = FileSystem.is_file(file_path)
        if not is_file_found:
            raise FileNotFoundError('file not found')

        try:
            with open(file_path, 'rb') as file:
                raw_data = file.read()
                raw_data.decode('utf-8')
            is_utf8 = True
        except UnicodeDecodeError:
            is_utf8 = False

        return is_utf8

    @staticmethod
    def get_file_type_from_format(file_path: str) -> FileType:
        """
        Determine the file type from the file format.

        :param file_path: str, path to the file
        :return: FileType, file type determined by the file format.
            If the file type is unknown, return FILE_TYPE_UNKNOWN.

        :raises FileNotFoundError: If the file is not found.
        """

        is_file_found = FileSystem.is_file(file_path)
        if not is_file_found:
            raise FileNotFoundError('file not found')

        is_utf8 = TexHandler.is_utf8_encoded(file_path)
        if is_utf8:
            latex2e_main_required_patterns = ['\\documentclass', '\\begin{document}', '\\end{document}']
            latex209_main_required_patterns = ['\\documentstyle', '\\begin{document}', '\\end{document}']

            with open(file_path, 'r', encoding='utf-8') as file:
                buffer = file.read()
                is_latex2e_main_format = all(pattern in buffer for pattern in latex2e_main_required_patterns)
                is_latex209_main_format = all(pattern in buffer for pattern in latex209_main_required_patterns)

                if is_latex2e_main_format:
                    file_type_category = FileType.FILE_TYPE_TEX_LATEX_2E_MAIN
                elif is_latex209_main_format:
                    file_type_category = FileType.FILE_TYPE_TEX_LATEX_209_MAIN
                else:
                    file_type_category = FileType.FILE_TYPE_UNKNOWN
        else:
            file_type_category = FileType.FILE_TYPE_UNKNOWN

        return file_type_category
