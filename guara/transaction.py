# Copyright (C) 2025-2026 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

"""
This module has all the transactions.
"""

from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from logging import Logger, getLogger
from pathlib import Path
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



LOGGER: Logger = getLogger(__name__)


@dataclass
class TransactionExecution:
    """
    Stores the execution history of a single transaction.

    The object intentionally stores serialized execution data instead of the
    Transaction instance itself so the history can be persisted independently
    from the current Application instance.
    """

    name: str
    module: str
    parameters: dict[str, Any] = field(default_factory=dict)
    status: str = "pending"
    started_at: str | None = None
    finished_at: str | None = None
    attempts: int = 0
    result: Any = None
    exception_type: str | None = None
    exception_message: str | None = None

    @property
    def identifier(self) -> str:
        """Returns a stable identifier for the transaction."""
        return f"{self.module}.{self.name}"

    def start(self) -> None:
        """Marks the transaction execution as started."""
        self.status = "running"
        self.started_at = _utc_now()

    def succeed(self, result: Any) -> None:
        """Marks the transaction execution as successful."""
        self.status = "succeeded"
        self.result = result
        self.finished_at = _utc_now()

    def fail(self, exception: Exception) -> None:
        """Marks the transaction execution as failed."""
        self.status = "failed"
        self.exception_type = type(exception).__name__
        self.exception_message = str(exception)
        self.finished_at = _utc_now()

    def skip(self) -> None:
        """Marks the transaction execution as skipped."""
        self.status = "skipped"
        self.finished_at = _utc_now()

    def to_dict(self) -> dict[str, Any]:
        """Returns the transaction execution as a dictionary."""
        return asdict(self)


@dataclass
class ExecutionHistory:
    """
    Represents the complete execution history of an Application.

    The history is independent from the Application execution pool and can be
    serialized to JSON for inspection, persistence, or future replay support.
    """

    application: str | None = None
    started_at: str | None = None
    finished_at: str | None = None
    status: str = "pending"
    transactions: list[TransactionExecution] = field(default_factory=list)

    def start(self) -> None:
        """Marks the application execution as started."""
        self.status = "running"
        self.started_at = _utc_now()

    def succeed(self) -> None:
        """Marks the application execution as successful."""
        self.status = "succeeded"
        self.finished_at = _utc_now()

    def fail(self) -> None:
        """Marks the application execution as failed."""
        self.status = "failed"
        self.finished_at = _utc_now()

    def add(self, execution: TransactionExecution) -> None:
        """Adds a transaction execution to the history."""
        self.transactions.append(execution)

    def to_dict(self) -> dict[str, Any]:
        """Returns the complete history as a dictionary."""
        return {
            "application": self.application,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "status": self.status,
            "transactions": [
                transaction.to_dict()
                for transaction in self.transactions
            ],
        }

    def dump(self, path: str | Path | None = None) -> str:
        """
        Serializes the execution history to JSON.

        Args:
            path: Optional file path. When provided, the JSON representation
                is also persisted to the specified file.

        Returns:
            The JSON representation of the execution history.
        """
        data = json.dumps(
            self.to_dict(),
            indent=2,
            default=_serialize_value,
        )

        if path is not None:
            Path(path).write_text(data, encoding="utf-8")

        return data


def _utc_now() -> str:
    """Returns the current UTC timestamp in ISO-8601 format."""
    return datetime.now(timezone.utc).isoformat()


def _serialize_value(value: Any) -> Any:
    """
    Converts values that are not directly JSON serializable into a safe
    representation for execution history.
    """
    try:
        json.dumps(value)
        return value
    except (TypeError, ValueError):
        return repr(value)


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
        Stores all transactions.
        """

        self._execution_history = ExecutionHistory(application=name)
        self._execution_history.start()

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
                "GUARA_DRY_RUN: True. Dry run is enabled. "
                "No action will be taken on drivers."
            )

        self._disabled = disabled

        if disabled:
            LOGGER.warning("Application disabled.")
            self._execution_history.status = "skipped"
            self._execution_history.finished_at = _utc_now()

    def __del__(self):
        if self._report_on_exit:
            LOGGER.info(self._report_on_exit)

    @property
    def result(self) -> Any:
        """
        It is the result data of the last transaction.
        """
        return self._result

    @property
    def history(self) -> ExecutionHistory:
        """
        Returns the execution history of the application.
        """
        return self._execution_history

    def dump_history(self, path: str | Path | None = None) -> str:
        """
        Dumps the execution history of the application.

        Args:
            path: Optional file path where the history should be persisted.

        Returns:
            The JSON representation of the execution history.
        """
        return self._execution_history.dump(path)

    def at(
        self,
        transaction: AbstractTransaction,
        **kwargs: dict[str, Any],
    ) -> Application:
        """
        Performs a transaction and records its execution history.

        Args:
            transaction: (AbstractTransaction): The web transaction handler.
            kwargs: (dict): It contains all the necessary data and parameters
             for the transaction.

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

        history = self._create_transaction_execution(
            self._transaction,
            kwargs,
            transaction_info,
        )

        history.start()

        for key, value in kwargs.items():
            if self._require_masking(key):
                value = SECRET_DEFAULT_VALUE
                kwargs[key] = value

        result_details = {
            "transaction": transaction_info,
            "parameteres": [{**kwargs}],
        }

        retries_on_failure = _retries_on_failure
        exception: Exception = None
        retries: int = 0

        while retries <= retries_on_failure:
            try:
                retries += 1
                history.attempts = retries

                self._result = self._transaction.act(**kwargs)

                history.succeed(self._result)

                LOGGER.info(
                    f"Transaction '{transaction_info}' succeded."
                )

                if GUARA_VERBOSE:
                    result_details["return"] = self._result
                    LOGGER.info(result_details)

                self._execution_history.succeed()

                return self

            except Exception as e:
                exception = e

                _retry_on_exceptions = (
                    self._transaction.retry_on_exceptions
                    or self._retry_on_exceptions
                )

                if not isinstance(e, _retry_on_exceptions):
                    LOGGER.warning(
                        f"Retry Ignored. Exception ({type(e)})"
                        f" not in retry list ({_retry_on_exceptions})."
                    )
                    break

                LOGGER.error(
                    f"Transaction '{transaction_info}' failed on attempt"
                    f" {retries} / {retries_on_failure + 1}."
                )
                LOGGER.exception(e)  # noqa

                if retries <= retries_on_failure and _pacing_time > 0:
                    LOGGER.info(
                        f"Waiting {_pacing_time}s for next retry."
                    )
                    time.sleep(_pacing_time)

        if exception:
            history.fail(exception)

            LOGGER.error(f"Transaction '{transaction_info}' failed.")

            if GUARA_VERBOSE:
                result_details["return"] = (
                    f"({type(exception)}) '{exception!s}'"
                )
                LOGGER.error(result_details)

            self._execution_history.fail()
            raise exception

    def _create_transaction_execution(
        self,
        transaction: AbstractTransaction,
        parameters: dict[str, Any],
        transaction_info: str,
    ) -> TransactionExecution:
        """
        Creates and registers an execution-history entry.

        Sensitive parameters are masked before they are stored in history.
        The original transaction parameters remain untouched until execution.
        """
        transaction_class = type(transaction)

        masked_parameters = {
            key: (
                SECRET_DEFAULT_VALUE
                if self._require_masking(key)
                else _serialize_value(value)
            )
            for key, value in parameters.items()
        }

        execution = TransactionExecution(
            name=transaction_class.__name__,
            module=transaction_class.__module__,
            parameters=masked_parameters,
        )

        self._execution_history.add(execution)

        return execution

    def _require_masking(self, key):
        return "secret" in key.lower() or "password" in key.lower() or "mask" in key.lower()

    def given(
        self,
        transaction: AbstractTransaction,
        **kwargs: dict[str, Any],
    ) -> Application:
        """
        Same as the `at` method. Introduced for better readability.

        Performs a transaction.

        Args:
            transaction: (AbstractTransaction): The web transaction handler.
            kwargs: (dict): It contains all the necessary data and parameters
             for the transaction.

        Returns:
            (Application)
        """
        return self.at(transaction, **kwargs)

    def when(
        self,
        transaction: AbstractTransaction,
        **kwargs: dict[str, Any],
    ) -> Application:
        """
        Same as the `at` method. Introduced for better readability.

        Performs a transaction.

        Args:
            transaction: (AbstractTransaction): The web transaction handler.
            kwargs: (dict): It contains all the necessary data and parameters
             for the transaction.

        Returns:
            (Application)
        """
        return self.at(transaction, **kwargs)

    def and_(
        self,
        transaction: AbstractTransaction,
        **kwargs: dict[str, Any],
    ) -> Application:
        """
        Same as the `at` method. Introduced for better readability.

        Performs a transaction.

        Args:
            transaction: (AbstractTransaction): The web transaction handler.
            kwargs: (dict): It contains all the necessary data and parameters
             for the transaction.

        Returns:
            (Application)
        """
        return self.at(transaction, **kwargs)

    def so(
        self,
        transaction: AbstractTransaction,
        **kwargs: dict[str, Any],
    ) -> Application:
        """
        Same as the `at` method. Introduced for better readability of
        transactions that represent post conditions.

        Example:
            given(HasStock).when(SellProduct).so(StockDecreased)

        Args:
            transaction: (AbstractTransaction): The web transaction handler.
            kwargs: (dict): It contains all the necessary data and parameters
             for the transaction.

        Returns:
            (Application)
        """
        return self.at(transaction, **kwargs)

    def execute(
        self,
        transaction: AbstractTransaction,
        **kwargs: dict[str, Any],
    ) -> Application:
        """
        Same as the `at` method. Introduced for better readability.

        Performs a transaction.

        Args:
            transaction: (AbstractTransaction): The web transaction handler.
            kwargs: (dict): It contains all the necessary data and parameters
             for the transaction.

        Returns:
            (Application)
        """
        return self.at(transaction, **kwargs)

    def asserts(
        self,
        assertion: IAssertion,
        expected: Any = None,
    ) -> Application:
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

    def expects(
        self,
        assertion: IAssertion,
        expected: Any = None,
    ) -> Application:
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

    def then(
        self,
        assertion: IAssertion,
        expected: Any = None,
    ) -> Application:
        """
        Asserting and validating the data by implementing the
        Strategy Pattern from the Gang of Four.

        Args:
            assertion: (IAssertion): The assertion logic to be used for validation.

        Returns:
            (Application)
        """
        return self.asserts(assertion, expected)

    def undo(self):
        """
        Reverts the actions performed by the `do` method when applicable.

        Returns:
            (Application)
        """
        if self._disabled:
            return self

        self._transaction_pool.reverse()

        for transaction in self._transaction_pool:
            LOGGER.info(
                f"Reverting transaction '{transaction.__name__}'"
            )
            transaction.revert_action()

        return self