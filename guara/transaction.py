# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

"""
This module has all the transactions.
"""

from typing import Any, Dict
from guara.it import IAssertion
from guara.utils import get_transaction_info, is_dry_run
from logging import getLogger, Logger
from guara.abstract_transaction import AbstractTransaction


LOGGER: Logger = getLogger("guara")


class Application:
    """
    This is the runner of the automation.
    """

    def __init__(self, driver: Any = None):
        """
        Initializing the application with a driver.

        Args:
            driver: (Any): This is the driver of the system being under test.
        """
        """
        Stores all transactions
        """
        self._transaction_pool: list[AbstractTransaction] = []
        if is_dry_run():
            self._driver = None
            return
        """
        It is the driver that has a transaction.
        """
        self._driver: Any = driver
        """
        It is the result data of the transaction.
        """
        self._result: Any = None
        """
        The web transaction handler.
        """
        self._transaction: AbstractTransaction
        """
        The assertion logic to be used for validation.
        """
        self._assertion: IAssertion

    @property
    def result(self) -> Any:
        """
        It is the result data of the transaction.
        """
        return self._result

    def at(self, transaction: AbstractTransaction, **kwargs: Dict[str, Any]) -> "Application":
        """
        Performing a transaction.

        Args:
            transaction: (AbstractTransaction): The web transaction handler.
            kwargs: (dict): It contains all the necessary data and parameters for the transaction.

        Returns:
            (Application)
        """
        self._transaction = transaction(self._driver)
        self._transaction_pool.append(self._transaction)
        transaction_info: str = get_transaction_info(self._transaction)
        LOGGER.info(f"Transaction: {transaction_info}")
        for key, value in kwargs.items():
            LOGGER.info(f" {key}: {value}")
        self._result = self._transaction.act(**kwargs)
        return self

    def when(self, transaction: AbstractTransaction, **kwargs: Dict[str, Any]) -> "Application":
        """
        Same as the `at` method. Introduced for better readability.

        Performing a transaction.

        Args:
            transaction: (AbstractTransaction): The web transaction handler.
            kwargs: (dict): It contains all the necessary data and parameters for the transaction.

        Returns:
            (Application)
        """
        return self.at(transaction, **kwargs)

    def then(self, transaction: AbstractTransaction, **kwargs: Dict[str, Any]) -> "Application":
        """
        Same as the `at` method. Introduced for better readability.

        Performing a transaction.

        Args:
            transaction: (AbstractTransaction): The web transaction handler.
            kwargs: (dict): It contains all the necessary data and parameters for the transaction.

        Returns:
            (Application)
        """
        return self.at(transaction, **kwargs)

    def asserts(self, assertion: IAssertion, expected: Any) -> "Application":
        """
        Asserting and validating the data by implementing the
        Strategy Pattern from the Gang of Four.

        Args:
            assertion: (IAssertion): The assertion logic to be used for validation.
            expected: (Any): The expected data.

        Returns:
            (Application)
        """
        self._assertion = assertion()
        self._assertion.validates(self._result, expected)
        return self

    def undo(self):
        """
        Reverts the actions performed by the `do` method when applicable

        Returns:
            (Application)
        """
        self._transaction_pool.reverse()
        for transaction in self._transaction_pool:
            LOGGER.info(f"Reverting '{transaction.__name__}' actions")
            transaction.revert_action()
        return self
