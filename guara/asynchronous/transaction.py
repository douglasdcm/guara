# Copyright (C) 2025-2026 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://guara.readthedocs.io/en/latest/

"""
The module that has all of the transactions.
"""

from __future__ import annotations

from logging import Logger, getLogger
from typing import Any, Coroutine

from guara.asynchronous.abstract_transaction import AbstractTransaction
from guara.asynchronous.it import IAssertion
from guara.constants import (
    GUARA_DRY_RUN,
    GUARA_VERBOSE,
    SECRET_DEFAULT_VALUE,
)
from guara.utils import get_transaction_info

LOGGER: Logger = getLogger(__name__)


class Application:
    def __init__(
        self,
        driver: Any = None,
        report_on_init=None,
        report_on_exit=None,
        disable=False,
        dry_run=False,
        name=None,
    ):
        """
        Initializing the application with a driver.

        Args:
            driver: (Any): It is a driver that is used to interact with the system being under test.

            report_on_init (str): The message to be reported when the application
             instance is initialized.

            report_on_exit (str): The message to be reported when the application
             instance is destroyed.
        """

        self._driver: Any = driver
        """
        It is the driver that has a transaction.
        """

        self._result: Any = None
        """
        It is the result data of the last transaction.
        """

        self._coroutines: list[dict[str, Coroutine[None, None, Any | None]]] = []
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

        self._kwargs: dict[str, Any] = None
        """
        It contains all the necessary data and parameters for the
        transaction.
        """

        self._transaction_name: str | None = None
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

        self._transaction: AbstractTransaction
        """
        The web transaction handler
        """

        self._disable = disable
        self._dry_run = dry_run

        if name:
            LOGGER.info(f"Application {name} running.")

        if report_on_init:
            LOGGER.info(report_on_init)

        self._report_on_exit = report_on_exit

        if GUARA_VERBOSE:
            LOGGER.warning("GUARA_VERBOSE enabled.")

    def __del__(self):
        if self._report_on_exit:
            LOGGER.info(self._report_on_exit)

    @property
    def result(self) -> Any:
        """
        It is the result data of the last transaction.
        """
        return self._result

    def at(
        self, transaction: AbstractTransaction, **kwargs: dict[str, Any]
    ) -> Application:
        """
        Executing each transaction.

        Args:
            transaction: (AbstractTransaction): The web transaction handler.
            kwargs: (dict): It contains all the necessary data and parameters for the transaction.

        Returns:
            (Application)
        """
        if self._disable:
            return self

        self._transaction = transaction(self._driver)
        self._kwargs = kwargs
        self._transaction_name = get_transaction_info(self._transaction)

        self._dry_run = self._dry_run if self._dry_run else GUARA_DRY_RUN

        if self._dry_run:
            LOGGER.warning("Dry run is enabled. No action will be taken on drivers.")
            if isinstance(
                self._transaction.execution_policy.return_on_dry_run, Exception
            ):
                raise self._transaction.execution_policy.return_on_dry_run
            return self

        coroutine: Coroutine[None, None, Any] = self._transaction.do(**kwargs)
        self._coroutines.append({self._TRANSACTION: coroutine})
        return self

    def when(
        self, transaction: AbstractTransaction, **kwargs: dict[str, Any]
    ) -> Application:
        """
        Same as the `at` method. Introduced for better readability.

        Performs a transaction.

        Args:
            transaction: (AbstractTransaction): The web transaction handler.
            kwargs: (dict): It contains all the necessary data and parameters for the transaction.

        Returns:
            (Application)
        """
        return self.at(transaction, **kwargs)

    def and_(
        self, transaction: AbstractTransaction, **kwargs: dict[str, Any]
    ) -> Application:
        """
        Same as the `at` method. Introduced for better readability.

        Performs a transaction.

        Args:
            transaction: (AbstractTransaction): The web transaction handler.
            kwargs: (dict): It contains all the necessary data and parameters for the transaction.

        Returns:
            (Application)
        """
        return self.at(transaction, **kwargs)

    def so(
        self, transaction: AbstractTransaction, **kwargs: dict[str, Any]
    ) -> Application:
        """
        Same as the `at` method. Introduced for better readability of transactions that
        represent post conditions. Performs a transaction.

        Example:
            given(HasStock).when(SellProduct).so(StockDecreased).preform()

        Args:
            transaction: (AbstractTransaction): The web transaction handler.
            kwargs: (dict): It contains all the necessary data and parameters for the transaction.

        Returns:
            (Application)
        """
        return self.at(transaction, **kwargs)

    def asserts(self, it: IAssertion, expected: Any) -> Application:
        """
        Asserting the data that is performed by the transaction
        against its expected value.

        Args:
            it: (IAssertion): The interface of the Assertion.
            expected: (Any): The expected data.

        Returns:
            (Application)
        """
        if self._disable:
            return self

        self._it = it()
        self._expected = expected
        coroutine: Coroutine[None, None, None] = self._it.validates(self, expected)
        self._coroutines.append({self._ASSERTION: coroutine})
        return self

    def then(self, it: IAssertion, expected: Any) -> Application:
        """
        Asserting the data that is performed by the transaction
        against its expected value.

        Args:
            it: (IAssertion): The interface of the Assertion.
            expected: (Any): The expected data.

        Returns:
            (Application)
        """
        return self.asserts(it, expected)

    async def perform(self) -> Application:
        """
        Executing all of the coroutines.

        Returns:
            (Application)
        """
        for index in range(0, len(self._coroutines), 1):
            if self._coroutines[index].get(self._TRANSACTION):
                await self.get_transaction(index)
            if self._coroutines[index].get(self._ASSERTION):
                await self.get_assertion(index)
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

        result_details = {}
        try:
            transaction: Coroutine[None, None, Any] = self._coroutines[index].get(
                self._TRANSACTION
            )

            for key, value in self._kwargs.items():
                if "secret" in key.lower() or "password" in key.lower():
                    value = SECRET_DEFAULT_VALUE
                    self._kwargs[key] = value

            result_details["transaction"] = self._transaction_name
            result_details["parameteres"] = {**self._kwargs}

            self._result = await transaction

            LOGGER.info(f"Transaction '{self._transaction_name}' succeded.")
            if GUARA_VERBOSE:
                result_details["return"] = self._result
                LOGGER.info(result_details)

        except Exception as e:
            LOGGER.info(f"Transaction '{self._transaction_name}' failed.")
            if GUARA_VERBOSE:
                result_details["return"] = f"({type(e)}) '{e!s}'"
                LOGGER.error(LOGGER.error(result_details))
            raise

    async def get_assertion(self, index: int) -> None:
        """
        Retrieving the assertion from the coroutine.

        Args:
            index: (int): The index of the current coroutine.

        Returns:
            (None)
        """
        assertion: Coroutine[None, None, None] = self._coroutines[index].get(
            self._ASSERTION
        )
        if assertion:
            return await assertion
