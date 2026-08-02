# Copyright (C) 2025-2026 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

"""
The module to be used to retrieve the information of the
transaction.
"""

from typing import Any
from logging import getLogger, Logger


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
