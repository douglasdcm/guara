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
from typing import Any, Callable, NoReturn

from guara.policy import TransactionExecutionPolicy

LOGGER: Logger = getLogger(__name__)


class AbstractTransaction:
    """
    Manages transaction execution by leveraging an injected driver.
    The driver can be any external dependency, such as a webdriver,
    database instance, or custom object.
    """

    execution_policy: TransactionExecutionPolicy = TransactionExecutionPolicy()
    preconditions: list[(Callable, dict)] | None = None
    postconditions: list[(Callable, dict)] | None = None

    def __init__(self, driver: Any = None):
        """
        Initializing the transaction which will allow it to interact
        with the driver.

        Args:
            driver: (Any): It is the driver that controls the user-interface.
        """
        self._driver: Any = driver

    def __post_init__(self):
        """Validates the class attributes assigned in the subclass."""
        self._validate_conditions(self.preconditions, condition_type="pre-condition")
        self._validate_conditions(self.postconditions, condition_type="pos-condition")

    def _validate_conditions(self, conditions, condition_type):
        if conditions is None:
            return

        _MINIMUM_ITEMS = 1
        if isinstance(conditions, list):
            for precondition in conditions:
                # String is allowed in case the precondition is defined inside the Transaction
                if (
                    len(conditions) > _MINIMUM_ITEMS
                    and isinstance(precondition[0], callable)
                    or isinstance(precondition[0], str)
                ):
                    if len(conditions) == _MINIMUM_ITEMS:
                        return
                    if len(conditions) == _MINIMUM_ITEMS + 1 and isinstance(
                        precondition[1], dict
                    ):
                        return
            raise TypeError(
                f"Invalid {condition_type} or post-condition ({type(conditions)})"
            )

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
