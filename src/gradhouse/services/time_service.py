# File: time_service.py
# Description: Time services.
#
# Copyright (c) 2025 Jason Stuber
# Licensed under the MIT License. See the LICENSE file for more details.

from datetime import datetime


class TimeService:
    """
    A class for timestamp comparison and conversion.
    """

    @staticmethod
    def is_iso_timestamp_newer(iso_timestamp1:str, iso_timestamp2:str) -> bool:
        """
        Determine if the first ISO 8601 timestamp is newer than another.

        :param iso_timestamp1: str, ISO timestamp
        :param iso_timestamp2: str, ISO timestamp
        :return: bool, True if the first timestamp is newer than the second, otherwise False.
        """

        dt1 = datetime.fromisoformat(iso_timestamp1)
        dt2 = datetime.fromisoformat(iso_timestamp2)

        return dt1 > dt2
