# Copyright (C) 2025-2026 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://guara.readthedocs.io/en/latest/

"""
It is the module where the interface of the transaction will
handle web transactions in an automated browser.
"""

from __future__ import annotations

from typing import Any

from guara.policy import TransactionPolicy


class AbstractTransaction:
    """
    Manages transaction execution by leveraging an injected driver.
    The driver can be any external dependency, such as a webdriver,
    database instance, or custom object.

    Args:
        driver (Any): It is the driver that controls the user-interface.

        return_on_dry_run (bool): Wheter the executions of the application hits the
         driver (False) or not (True).

        execution_policy (TransactionExecutionPolicy): Defines how the transaction is executed.

    Documentation: https://guara.readthedocs.io/en/latest/

    """

    return_on_dry_run = None
    """(bool) Wheter the executions of the application hits the driver (False) or not (True)."""

    execution_policy = TransactionPolicy()
    """Defines how the transaction is executed."""

    @property
    def __name__(self) -> property:
        """
        The name of the transaction being implemented.
        """
        return self.__class__.__name__

    def __init__(self, driver: Any = None):
        """
        Initializing the transaction which will allow it to interact
        with the driver.

        Args:
            driver: (Any): It is the driver that controls a user-interface.
        """
        self._driver: Any = driver

    async def do(self, **kwargs: dict[str, Any]) -> Any:
        """
        It performs a specific transaction

        Args:
            kwargs: (dict): It contains all the necessary data and parameters for the transaction.

        Returns:
            (Any | NoReturn)

        Raises:
            NotImplementedError: The method is not implemented in the subclass.
        """
        raise NotImplementedError
