# File: submission_handler.py
# Description: Submission methods.
#
# Copyright (c) 2025 Jason Stuber
# Licensed under the MIT License. See the LICENSE file for more details.

from gradhouse.file.handler.archive_handler import ArchiveHandler

from gradhouse.file.file_handler import FileHandler
from gradhouse.file.file_system import FileSystem
from gradhouse.file.file_type import FileType

from gradhouse.services.hash_service import HashType

from .patterns import Patterns
from .submission_type import SubmissionType


class SubmissionHandler:
    """
    Submission handler methods
    """

    @staticmethod
    def get_submission_type_using_extension(submission_file_list: list[str]) -> SubmissionType:
        """
        Get the submission type category from the contents extensions.

        This method inspects the list of files in the submission and determines the overall submission type
        based on the detected file types. The classification is as follows:

        - If all files are PostScript (.ps), returns SUBMISSION_TYPE_POSTSCRIPT.
        - If all files are PDF (.pdf), returns SUBMISSION_TYPE_PDF.
        - If at least one TeX/LaTeX main file is present and all other files are recognized as TeX/LaTeX
          supporting files, returns SUBMISSION_TYPE_TEX.
        - If any file is unrecognized or not associated with the detected main type, returns SUBMISSION_TYPE_UNKNOWN.

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
        elif {FileType.FILE_TYPE_PDF} == file_types:
            # pdf submission type
            submission_type = SubmissionType.SUBMISSION_TYPE_PDF
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

    @staticmethod
    def generate_submission_entry(file_path: str, bulk_archive_hash: str) -> tuple[str, dict]:
        """
        Generate the key value pair for an arXiv submission entry

        :param file_path: str, file path to the submission entry
        :param bulk_archive_hash: str, SHA256 hash of the bulk archive entry that contained the submission
        :return: tuple[str, dict], key, value pair for the submission entry
            The key is the SHA256 hash for the submission
            The value is a dictionary with the fields 'metadata' and 'origin'.
            If the submission has an error then the 'diagnostics' field will be created with entry 'error_list'
            that lists the corresponding errors.

        :raises FileNotFoundError: if the submission entry does not exist
        """

        hash_types = [HashType.HASH_TYPE_MD5, HashType.HASH_TYPE_SHA256]

        if not FileSystem.is_file(file_path):
            raise FileNotFoundError(f"File '{file_path}' not found.")

        submission_errors = Patterns.check_submission(file_path)
        url = Patterns.generate_url_for_submission_filename(file_path)
        metadata = FileHandler.get_metadata(file_path, hash_types=hash_types)

        submission_key = metadata['hash']['SHA256']

        if len(submission_errors) > 0:
            submission_type = SubmissionType.SUBMISSION_TYPE_UNKNOWN
        else:
            if metadata['file_type'] in [FileType.FILE_TYPE_PDF.value]:
                submission_type = SubmissionType.SUBMISSION_TYPE_PDF
            else:
                if metadata['file_type'] in [FileType.FILE_TYPE_ARCHIVE_GZ.value, FileType.FILE_TYPE_ARCHIVE_TGZ.value]:
                    archive_contents = ArchiveHandler.list_contents(file_path)
                    submission_type = SubmissionHandler.get_submission_type_using_extension(archive_contents)
                else:
                    submission_type = SubmissionType.SUBMISSION_TYPE_UNKNOWN

        metadata['submission_type_by_extension'] = submission_type.value

        if len(submission_errors) == 0 and submission_type == SubmissionType.SUBMISSION_TYPE_UNKNOWN:
            submission_errors.append('Unknown submission type')

        submission_entry = {
            'metadata': metadata,
            'origin': {
                'url': url,
                'bulk_archive_hash': bulk_archive_hash
            }
        }

        if len(submission_errors) > 0:
            submission_entry['diagnostics'] = {'error_list': submission_errors}

        return submission_key, submission_entry
