# Copyright (C) 2025-2026 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://guara.readthedocs.io/en/latest/

"""
It is the module where the AbstractTransaction will handle
web transactions in an automated browser.
"""

from __future__ import annotations

from logging import Logger, getLogger
from typing import Any, ClassVar, NoReturn

from guara.policy import TransactionExecutionPolicy

LOGGER: Logger = getLogger(__name__)


class AbstractTransaction:
    """
    Manages transaction execution by leveraging an injected driver.
    The driver can be any external dependency, such as a webdriver,
    database instance, or custom object.

    Args:
        driver: (Any): It is the driver that controls the user-interface.

        requires: list[AbstractTransaction]: A state required by the transaction before execution.

        ensures: list[AbstractTransaction]: A state ensured by the transaction after execution.

        execution_policy: TransactionExecutionPolicy: Defined how the transaction is executed.

    Documentation: https://guara.readthedocs.io/en/latest/
    """

    requires: list[AbstractTransaction] = []
    """A state required by the transaction before execution."""

    ensures: list[AbstractTransaction] = []
    """A state ensured by the transaction after execution."""

    execution_policy: TransactionExecutionPolicy = TransactionExecutionPolicy()
    """Defined how the transaction is executed."""

    def __init__(self, driver: Any = None):
        self._driver: Any = driver

    @property
    def __name__(self) -> property:
        """
        The name of the transaction

        Returns:
            (str) The name of the transaction being implemented.
        """
        return self.__class__.__name__

    def do(self, **kwargs: dict[str, Any]) -> Any:
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

    def act(self, **kwargs: dict[str, Any]) -> Any:
        return self.do(**kwargs)

    def undo(self):
        """
        Reverts the actions performed by the method `do`

        Returns:
            (NoReturn)
        """

    def revert_action(self) -> NoReturn:
        return self.undo()
