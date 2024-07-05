#!/usr/bin/env python3
"""0. Regex-ing."""

import re
import logging
from typing import List

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


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


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class."""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initialize the RedactingFormatter instance.

        Args:
            fields (List[str]): List of strings representing
            all fields to obfuscate.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record, filtering sensitive information.

        Args:
            record (logging.LogRecord): The log record to format.

        Returns:
            str: The formatted log record with specified fields obfuscated.
        """
        original_message = super().format(record)
        return filter_datum(
            self.fields, self.REDACTION, original_message, self.SEPARATOR)

def get_logger() -> logging.Logger:
    """Get a logger named user_data."""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)
    return logger
