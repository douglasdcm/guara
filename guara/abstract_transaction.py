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
from typing import Any, NoReturn

from guara.constants import GUARA_DRY_RUN
from guara.policy import TransactionExecutionPolicy

LOGGER: Logger = getLogger(__name__)


class AbstractTransaction:
    """
    Manages transaction execution by leveraging an injected driver.
    The driver can be any external dependency, such as a webdriver,
    database instance, or custom object.
    """

    policy: TransactionExecutionPolicy = TransactionExecutionPolicy()

    def __init__(self, driver: Any = None):
        """
        Initializing the transaction which will allow it to interact
        with the driver.

        Args:
            driver: (Any): It is the driver that controls the user-interface.
        """
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
        if GUARA_DRY_RUN:
            if isinstance(self.policy.return_on_dry_run, Exception):
                raise self.policy.return_on_dry_run
            return self.policy.return_on_dry_run
        return self.do(**kwargs)

    def undo(self):
        """
        Reverts the actions performed by the method `do`

        Returns:
            (NoReturn)
        """

    def revert_action(self) -> NoReturn:
        if GUARA_DRY_RUN:
            return
        return self.undo()
