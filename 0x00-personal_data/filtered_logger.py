#!/usr/bin/env python3
"""0. Regex-ing."""


import re
from typing import List


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str) -> str:
    """
    Obfuscate specified fields in a log message.

    Args:
        fields (List[str]): List of strings representing
        all fields to obfuscate.
        redaction (str): String representing by what the
        field will be obfuscated.
        message (str): String representing the log line.
        separator (str): String representing by which character
        fields are separated in the log line.

    Returns:
        str: The log message with specified fields obfuscated.
    """
    return re.sub(
        f'({"|".join(fields)})=[^{separator}]+',
        lambda match: f"{match.group(1)}={redaction}",
        message
    )
