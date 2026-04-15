# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

"""
This module has all the transactions.
"""

from typing import Any, Dict
from guara.it import IAssertion
from guara.utils import get_transaction_info, is_dry_run, get_retries_on_failure
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
        self._transaction_pool: list[AbstractTransaction] = []
        """
        Stores all transactions
        """
        if is_dry_run():
            self._driver = None
            return
        self._driver: Any = driver
        """
        It is the driver that has a transaction.
        """
        self._result: Any = None
        """
        It is the result data of the last transaction.
        """
        self._transaction: AbstractTransaction
        """
        The web transaction handler.
        """
        self._assertion: IAssertion
        """
        The assertion logic to be used for validation.
        """

    @property
    def result(self) -> Any:
        """
        It is the result data of the last transaction.
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
        LOGGER.info(f"Running transaction '{transaction_info}'")
        for key, value in kwargs.items():
            LOGGER.info(f" {key}: {value}")

        retries_on_failure = get_retries_on_failure()
        exception: Exception = None
        retries: int = -1
        while retries < retries_on_failure:
            try:
                self._result = self._transaction.act(**kwargs)
                return self
            except Exception as e:
                LOGGER.error(f"Transaction '{transaction_info}' failed on attempt {retries + 1}")
                LOGGER.exception(str(e))
                retries += 1
                exception = e

        raise exception

    def given(self, transaction: AbstractTransaction, **kwargs: Dict[str, Any]) -> "Application":
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

    def and_(self, transaction: AbstractTransaction, **kwargs: Dict[str, Any]) -> "Application":
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

    def execute(self, transaction: AbstractTransaction, **kwargs: Dict[str, Any]) -> "Application":
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

    def asserts(self, assertion: IAssertion, expected: Any = None) -> "Application":
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

    def expects(self, assertion: IAssertion, expected: Any = None) -> "Application":
        """
        Asserting and validating the data by implementing the
        Strategy Pattern from the Gang of Four.

        Args:
            assertion: (IAssertion): The assertion logic to be used for validation.
            expected: (Any): The expected data.

        Returns:
            (Application)
        """
        return self.asserts(assertion, expected)

    def then(self, assertion: IAssertion, expected: Any = None) -> "Application":
        """
        Asserting and validating the data by implementing the
        Strategy Pattern from the Gang of Four.

        Args:
            assertion: (IAssertion): The assertion logic to be used for validation.
            expected: (Any): The expected data.

        Returns:
            (Application)
        """
        return self.asserts(assertion, expected)

    def undo(self):
        """
        Reverts the actions performed by the `do` method when applicable

        Returns:
            (Application)
        """
        self._transaction_pool.reverse()
        for transaction in self._transaction_pool:
            LOGGER.info(f"Reverting transaction '{transaction.__name__}'")
            transaction.revert_action()
        return self
