#!/usr/bin/env python3
"""
Module for data filtering with log obfuscation
"""

import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    Obfuscates specified fields in a log message.

    Args:
        fields (List[str]): List of fields to obfuscate in the message.
        redaction (str): The string to replace the field values with.
        message (str): The original log message to be obfuscated.
        separator (str): The character that separates fields in
                         the log message.

    Returns:
        str: The obfuscated log message.
    """
    return (re.sub(f'({"|".join(fields)})=[^{separator}]*',
                   lambda m: f"{m.group(1)}={redaction}", message))
