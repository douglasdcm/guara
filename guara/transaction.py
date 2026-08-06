# Copyright (C) 2025-2026 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

"""
This module has all the transactions.
"""

from __future__ import annotations

import time
from logging import Logger, getLogger
from typing import Any

from guara.abstract_transaction import AbstractTransaction
from guara.constants import (
    GUARA_DISABLE_LOGS,
    GUARA_DRY_RUN,
    GUARA_PACING_TIME,
    GUARA_RETRIES_ON_FAILURE,
    GUARA_VERBOSE,
    SECRET_DEFAULT_VALUE,
)
from guara.it import IAssertion
from guara.utils import get_transaction_info

LOGGER: Logger = getLogger(__name__)


class Application:

    def __init__(
        self,
        driver: Any = None,
        report_on_init: str | None = None,
        report_on_exit: str | None = None,
        retry_on_exceptions: tuple[Exception] = (Exception),
        disabled: bool = False,
        name: str | None = None,
    ):
        """
        Initializing the application with a driver.

        Args:
            driver: (Any): This is the driver of the system being under test.

            report_on_init (str): The message to be reported when the application
             instance is initialized.

            report_on_exit (str): The message to be reported when the application
             instance is destroyed.

            retry_on_exceptions (tuple(Exception)): the listo fo the Exceptions
             to be retried.

            disabled (bool): disable the application so that no action
             is excuted (feature flagging).

            name (str): the name to identify the application in logs.
        """
        self._transaction_pool: list[AbstractTransaction] = []
        """
        Stores all transactions
        """

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
        if name:
            LOGGER.info(f"Application {name} running.")

        if report_on_init:
            LOGGER.info(report_on_init)

        self._report_on_exit: str = report_on_exit
        """
        The message to be reported when the application instance is destroyed.
        """

        self._retry_on_exceptions = retry_on_exceptions

        if GUARA_VERBOSE:
            LOGGER.warning(
                {
                    "GUARA_DISABLE_LOGS": GUARA_DISABLE_LOGS,
                    "GUARA_DRY_RUN": GUARA_DRY_RUN,
                    "GUARA_PACING_TIME": GUARA_PACING_TIME,
                    "GUARA_RETRIES_ON_FAILURE": GUARA_RETRIES_ON_FAILURE,
                    "GUARA_VERBOSE": GUARA_VERBOSE,
                }
            )

        if GUARA_DRY_RUN:
            LOGGER.warning(
                "GUARA_DRY_RUN: True. Dry run is enabled. No action will be taken on drivers."
            )

        self._disabled = disabled
        if disabled:
            LOGGER.warning("Application disabled.")

    def __del__(self):
        if self._report_on_exit:
            LOGGER.info(self._report_on_exit)

    @property
    def result(self) -> Any:
        """
        It is the result data of the last transaction.
        """
        return self._result

    def at(self, transaction: AbstractTransaction, **kwargs: dict[str, Any]) -> Application:
        """
        Performs a transaction.

        Args:
            transaction: (AbstractTransaction): The web transaction handler.
            kwargs: (dict): It contains all the necessary data and parameters for the transaction.

        Returns:
            (Application)
        """
        if self._disabled:
            return self

        self._transaction = transaction(self._driver)
        _pacing_time = (
            self._transaction.pacing_time
            if self._transaction.pacing_time is not None
            else GUARA_PACING_TIME
        )

        _retries_on_failure = (
            self._transaction.retries_on_failure
            if self._transaction.retries_on_failure is not None
            else GUARA_RETRIES_ON_FAILURE
        )

        self._transaction_pool.append(self._transaction)
        transaction_info: str = get_transaction_info(self._transaction)

        for key, value in kwargs.items():
            if "secret" in key.lower() or "password" in key.lower():
                value = SECRET_DEFAULT_VALUE
                kwargs[key] = value

        result_details = {"transaction": transaction_info, "parameteres": [{**kwargs}]}

        retries_on_failure = _retries_on_failure
        exception: Exception = None
        retries: int = 0
        while retries <= retries_on_failure:
            try:
                self._result = self._transaction.act(**kwargs)
                LOGGER.info(f"Transaction '{transaction_info}' succeded.")

                if GUARA_VERBOSE:
                    result_details["return"] = self._result
                    LOGGER.info(result_details)

                return self
            except Exception as e:
                exception = e
                _retry_on_exceptions = (
                    self._transaction.retry_on_exceptions or self._retry_on_exceptions
                )
                if not isinstance(e, _retry_on_exceptions):
                    LOGGER.warning(
                        f"Retry Ignored. Exception ({type(e)})"
                        f" not in retry list ({_retry_on_exceptions})."
                    )
                    break

                else:
                    retries += 1
                    LOGGER.error(
                        f"Transaction '{transaction_info}' failed on attempt"
                        f" {retries} / {retries_on_failure + 1}."
                    )
                    LOGGER.exception(e) # noqa
                    if retries <= retries_on_failure and _pacing_time > 0:
                        LOGGER.info(f"Waiting {_pacing_time}s for next retry.")
                        time.sleep(_pacing_time)

        if exception:
            LOGGER.error(f"Transaction '{transaction_info}' failed.")
            if GUARA_VERBOSE:
                result_details["return"] = f"({type(exception)}) '{exception!s}'"
                LOGGER.error(result_details)
            raise exception

    def given(self, transaction: AbstractTransaction, **kwargs: dict[str, Any]) -> Application:
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

    def when(self, transaction: AbstractTransaction, **kwargs: dict[str, Any]) -> Application:
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

    def and_(self, transaction: AbstractTransaction, **kwargs: dict[str, Any]) -> Application:
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

    def so(self, transaction: AbstractTransaction, **kwargs: dict[str, Any]) -> Application:
        """
        Same as the `at` method. Introduced for better readability of transactions that
        represent post conditions. Performs a transaction.

        Example:
            given(HasStock).when(SellProduct).so(StockDecreased)

        Args:
            transaction: (AbstractTransaction): The web transaction handler.
            kwargs: (dict): It contains all the necessary data and parameters for the transaction.

        Returns:
            (Application)
        """
        return self.at(transaction, **kwargs)

    def execute(self, transaction: AbstractTransaction, **kwargs: dict[str, Any]) -> Application:
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

    def asserts(self, assertion: IAssertion, expected: Any = None) -> Application:
        """
        Asserting and validating the data by implementing the
        Strategy Pattern from the Gang of Four.

        Args:
            assertion: (IAssertion): The assertion logic to be used for validation.
            expected: (Any): The expected data.

        Returns:
            (Application)
        """
        if self._disabled:
            return self

        self._assertion = assertion()
        self._assertion.validates(self._result, expected)
        return self

    def expects(self, assertion: IAssertion, expected: Any = None) -> Application:
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

    def then(self, assertion: IAssertion, expected: Any = None) -> Application:
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
        if self._disabled:
            return self

        self._transaction_pool.reverse()
        for transaction in self._transaction_pool:
            LOGGER.info(f"Reverting transaction '{transaction.__name__}'")
            transaction.revert_action()
        return self
