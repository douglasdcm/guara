# Copyright (C) 2025-2026 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://guara.readthedocs.io/en/latest/

"""
The module to be used to retrieve the information of the
transaction.
"""

from logging import Logger, getLogger
from os import getenv
from typing import Any

LOGGER: Logger = getLogger(__name__)


def get_transaction_info(transaction: Any) -> str:
    """
    Retrieving the information of a transaction.

    Args:
        transaction: Any: The transaction object.

    Returns:
        string
    """
    return f"{transaction.__name__}"


def convert_variable_to_integer(variable, verbose) -> int:
    env_var = getenv(variable, "0")
    try:
        result = int(env_var)
        if result < 0:
            raise ValueError
        return result

    except (ValueError, TypeError):
        if verbose:
            LOGGER.warning(
                f"Invalid {variable} value: '{env_var}'."
                " Expected a positive integer. Defaulting to 0."
            )
        return 0
