"""
The module to be used to retrieve the information of the
transaction.

Authors:
    douglasdcm
    RonaldTheodoro
"""
from typing import Any


def get_transaction_info(transaction: Any) -> str:
    """
    Retrieving the information of a transaction.

    Parameters:
        transaction: Any: The transaction object.

    Returns:
        string
    """
    module_name: str = ".".join(transaction.__module__.split(".")[-1:])
    return f"{module_name}.{transaction.__name__}"
