# File: submission_handler.py
# Description: Submission methods.
#
# Copyright (c) 2025 Jason Stuber
# Licensed under the MIT License. See the LICENSE file for more details.

from gradhouse.file.file_handler import FileHandler
from gradhouse.file.file_type import FileType

from .submission_type import SubmissionType


class SubmissionHandler:
    """
    Submission handler methods
    """

    @staticmethod
    def get_submission_type_using_extension(submission_file_list: list[str]) -> SubmissionType:
        """
        Get the submission type category from the contents extensions.
        :param submission_file_list: str, list of files in the submission
        :return: SubmissionType, matching submission type category
        """

        tex_types = {FileType.FILE_TYPE_TEX_TEX, FileType.FILE_TYPE_TEX_LATEX_209_MAIN,
                     FileType.FILE_TYPE_TEX_LATEX_2E_MAIN}
        tex_supporting_types = {FileType.FILE_TYPE_TEX_LOG, FileType.FILE_TYPE_TEX_FIG, FileType.FILE_TYPE_IMAGE_GIF,
                                FileType.FILE_TYPE_IMAGE_PNG, FileType.FILE_TYPE_IMAGE_JPG, FileType.FILE_TYPE_TEX_BIB,
                                FileType.FILE_TYPE_TEX_CLO, FileType.FILE_TYPE_TEX_BST, FileType.FILE_TYPE_TEX_TOC,
                                FileType.FILE_TYPE_TEX_CLS, FileType.FILE_TYPE_TEX_BBL, FileType.FILE_TYPE_POSTSCRIPT_EPSF,
                                FileType.FILE_TYPE_TEX_PSTEX_T, FileType.FILE_TYPE_TEX_PSTEX, FileType.FILE_TYPE_TEX_STY,
                                FileType.FILE_TYPE_TEX_LATEX_209_MAIN, FileType.FILE_TYPE_TEX_LATEX_2E_MAIN,
                                FileType.FILE_TYPE_TEX_TEX, FileType.FILE_TYPE_PDF, FileType.FILE_TYPE_POSTSCRIPT_PS,
                                FileType.FILE_TYPE_POSTSCRIPT_EPSI, FileType.FILE_TYPE_POSTSCRIPT_EPS}

        file_types = []
        for filename in submission_file_list:
            current_file_type_list = FileHandler.get_file_type_from_extension(filename)
            if len(current_file_type_list) == 0:
                file_types.append(FileType.FILE_TYPE_UNKNOWN)
            else:
                file_types.extend(current_file_type_list)
        file_types = set(file_types)

        if {FileType.FILE_TYPE_POSTSCRIPT_PS} == file_types:
            # postscript submission type
            submission_type = SubmissionType.SUBMISSION_TYPE_POSTSCRIPT
        elif len(tex_types & file_types) > 0:
            # potential TeX or LaTeX submission type
            residual = file_types - tex_supporting_types
            if len(residual) == 0:
                # all file types are TeX / LaTeX associated
                submission_type = SubmissionType.SUBMISSION_TYPE_TEX
            else:
                # at least one file type is not TeX or LaTeX associated
                submission_type = SubmissionType.SUBMISSION_TYPE_UNKNOWN
        else:
            # file types are not associated with a known submission type
            submission_type = SubmissionType.SUBMISSION_TYPE_UNKNOWN

        return submission_type
