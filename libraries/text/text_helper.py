#!/usr/bin/python3
"""Text Helper"""


import re
import unicodedata


class TextHelper:
    """Class to help usage of Text"""

    @staticmethod
    def is_none(
        text: str
    ):
        """Specify if None"""

        if text is None:
            return True

        if text == 'None':
            return True

        return False

    @staticmethod
    def sanitize(
        text: str
    ) -> str:
        """Sanitize specified text"""

        if text is None:
            return text

        # Normalize text
        result = unicodedata.normalize('NFKD', text).encode(
            'ascii', 'ignore').decode()

        # Remove forbidden characters
        result = re.sub(r'[\\/:*?"<>|]', '', result)

        # Trim
        result = result.strip()

        # Replace spaces by _
        result = re.sub(r'\s+', '_', result)

        return result
