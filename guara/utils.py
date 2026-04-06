# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

"""
The module to be used to retrieve the information of the
transaction.
"""
import os
from typing import Any
from logging import getLogger, Logger

LOGGER: Logger = getLogger(__name__)


def is_dry_run():
    result = os.getenv("DRY_RUN", "false").lower() == "true"
    if result:
        LOGGER.warning(f"DRY_RUN: {result}. Dry run is enabled. No action was taken on drivers.")
    return result


def get_retries_on_failure() -> int:
    try:
        # Get the value, default to "0" if not found
        raw_value = os.getenv("RETRIES_ON_FAILURE", "0")
        result = int(raw_value)

        if result > 0:
            LOGGER.warning(
                f"RETRIES_ON_FAILURE: {result}. \
                           Transactions will be retried on failure."
            )
            return result

        # If it's 0 or negative, we treat it as "no retries"
        return 0

    except (ValueError, TypeError):
        # If user entered "abc", log an error and default to 0 so the test can still run
        LOGGER.warning(
            f"Invalid RETRIES_ON_FAILURE value: \
                     '{os.getenv('RETRIES_ON_FAILURE')}'. Expected an integer. Defaulting to 0."
        )
        return 0


def get_transaction_info(transaction: Any) -> str:
    """
    Retrieving the information of a transaction.

    Args:
        transaction: Any: The transaction object.

    Returns:
        string
    """
    module_name: str = ".".join(transaction.__module__.split(".")[-1:])
    return f"{module_name}.{transaction.__name__}"
