#!/usr/bin/env python3
"""
Module for data filtering with log obfuscation
"""

import os
import mysql.connector
import re
from typing import List
import logging


# Define PII_FIELDS as a tuple with fields to be redacted in logs
PII_FIELDS = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Format the log record, filtering PII fields."""
        record.msg = (filter_datum(self.fields, self.REDACTION,
                                   record.getMessage(), self.SEPARATOR))
        return super().format(record)


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


def get_logger() -> logging.Logger:
    """Creates and configures a logger with redaction for PII fields."""
    # Create a logger named 'user_data' with INFO level
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False  # Prevent logger propagating to to other loggers

    # Create StreamHandler, set formatter to RedactingFormatter with PII_FIELDS
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(fields=PII_FIELDS))

    # Add the handler to the logger
    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Connects to the MySQL database."""
    # Connect to the MySQL database
    return mysql.connector.connect(
        host=os.getenv("PERSONAL_DATA_DB_HOST", "localhost"),
        database=os.getenv("PERSONAL_DATA_DB_NAME"),
        user=os.getenv("PERSONAL_DATA_DB_USERNAME", "root"),
        password=os.getenv("PERSONAL_DATA_DB_PASSWORD", ""))


def main() -> None:
    """Main function to retrieve and log filtered user data..
    """
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    logger = get_logger()

    for row in cursor:
        # Log each row of the users table
        message = "; ".join([f"{key}={value}" for key, value in row.items()])
        logger.info(message)

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
