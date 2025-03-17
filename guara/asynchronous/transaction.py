# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

"""
The module that has all of the transactions.
"""

from typing import Any, List, Dict, Coroutine, Union
from guara.asynchronous.it import IAssertion
from guara.utils import get_transaction_info
from logging import getLogger, Logger
from guara.asynchronous.abstract_transaction import AbstractTransaction

LOGGER: Logger = getLogger("guara")


class Application:
    """
    The runner of the automation.
    """

    def __init__(self, driver: Any = None):
        """
        Initializing the application with a driver.

        Args:
            driver: (Any): It is a driver that is used to interact with the system being under test.
        """
        self._driver: Any = driver
        """
        It is the driver that has a transaction.
        """
        self._result: Any = None
        """
        It is the result data of the transaction.
        """
        self._coroutines: List[Dict[str, Coroutine[None, None, Union[Any, None]]]] = []
        """
        The list of transactions that are performed.
        """
        self._TRANSACTION: str = "transaction"
        """
        Transaction header
        """
        self._ASSERTION: str = "assertion"
        """
        Assertion header
        """
        self._kwargs: Dict[str, Any] = None
        """
        It contains all the necessary data and parameters for the
        transaction.
        """
        self._transaction_name: str = None
        """
        The name of the transaction.
        """
        self._it: IAssertion = None
        """
        The interface of the Assertion
        """
        self._expected: Any = None
        """
        The expected data
        """
        self.__transaction: AbstractTransaction
        """
        The web transaction handler
        """

    @property
    def result(self) -> Any:
        """
        It is the result data of the transaction.
        """
        return self._result

    def at(self, transaction: AbstractTransaction, **kwargs: Dict[str, Any]) -> "Application":
        """
        Executing each transaction.

        Args:
            transaction: (AbstractTransaction): The web transaction handler.
            kwargs: (dict): It contains all the necessary data and parameters for the transaction.

        Returns:
            (Application)
        """
        self.__transaction = transaction(self._driver)
        self._kwargs = kwargs
        self._transaction_name = get_transaction_info(self.__transaction)
        coroutine: Coroutine[None, None, Any] = self.__transaction.do(**kwargs)
        self._coroutines.append({self._TRANSACTION: coroutine})
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

    def asserts(self, it: IAssertion, expected: Any) -> "Application":
        """
        Asserting the data that is performed by the transaction
        against its expected value.

        Args:
            it: (IAssertion): The interface of the Assertion.
            expected: (Any): The expected data.

        Returns:
            (Application)
        """
        self._it = it()
        self._expected = expected
        coroutine: Coroutine[None, None, None] = self._it.validates(self, expected)
        self._coroutines.append({self._ASSERTION: coroutine})
        return self

    async def perform(self) -> "Application":
        """
        Executing all of the coroutines.

        Returns:
            (Application)
        """
        for index in range(0, len(self._coroutines), 1):
            (await self.get_assertion(index) if not await self.get_transaction(index) else None)
        self._coroutines.clear()
        return self

    async def get_transaction(self, index: int) -> bool:
        """
        Retrieving the transaction from the coroutine.

        Args:
            index: (int): The index of the current coroutine.

        Returns:
            (bool)
        """
        transaction: Coroutine[None, None, Any] = self._coroutines[index].get(self._TRANSACTION)
        if transaction:
            LOGGER.info(f"Transaction: {self._transaction_name}")
            for key, value in self._kwargs.items():
                LOGGER.info(f" {key}: {value}")
            self._result = await transaction
            return True
        return False

    async def get_assertion(self, index: int) -> None:
        """
        Retrieving the assertion from the coroutine.

        Args:
            index: (int): The index of the current coroutine.

        Returns:
            (None)
        """
        LOGGER.info(f"Assertion: {self._it.__name__}")
        LOGGER.info(f" Actual  : {self._result}")
        LOGGER.info(f" Expected: {self._expected}")
        assertion: Coroutine[None, None, None] = self._coroutines[index].get(self._ASSERTION)
        if assertion:
            return await assertion
