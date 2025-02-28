# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

"""
The module to be used to retrieve the information of the
transaction.
"""

from typing import Any


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
