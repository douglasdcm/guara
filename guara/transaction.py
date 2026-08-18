# Copyright (C) 2025-2026 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://guara.readthedocs.io/en/latest/

"""
This module has all the transactions.
"""

from __future__ import annotations

import copy
import importlib
import inspect
import json
import sys
import time
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from logging import Logger, getLogger
from pathlib import Path
from typing import Any

from guara.abstract_transaction import AbstractTransaction
from guara.constants import (
    GUARA_DRY_RUN,
    GUARA_PACING_TIME,
    GUARA_RETRIES_ON_FAILURE,
    GUARA_VERBOSE,
    SECRET_DEFAULT_VALUE,
)
from guara.it import IAssertion
from guara.policy import ApplicationPolicy, TransactionPolicy
from guara.utils import get_transaction_info

LOGGER: Logger = getLogger(__name__)


class ReplayError(Exception):
    """Raised when an execution history cannot be replayed."""


class PreconditionError(Exception):
    """Raised when a pre-conditon cannot be executed."""


class PosconditionError(Exception):
    """Raised when a pos-conditon cannot be executed."""


def _get_module_path(transaction: AbstractTransaction) -> str:
    """Return the complete Python module path for a transaction."""
    file_path = Path(inspect.getfile(type(transaction))).resolve()

    for search_path in map(Path, sys.path):
        try:
            relative_path = file_path.relative_to(search_path.resolve())
        except ValueError:
            continue

        return ".".join(relative_path.with_suffix("").parts)

    raise ImportError(f"Could not determine module path for {file_path}")


@dataclass
class TransactionExecution:
    """
    Stores the execution history of a single transaction.

    The object intentionally stores serialized execution data instead of the
    Transaction instance itself so the history can be persisted independently
    from the current Application instance.
    """

    id: str
    policy: TransactionPolicy
    name: str
    module: str
    parameters: dict[str, Any] = field(default_factory=dict)
    status: str = "pending"
    started_at: str | None = None
    finished_at: str | None = None
    attempts: int = 0
    exception_type: str | None = None
    exception_message: str | None = None
    replayable: bool = True

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

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> TransactionExecution:
        """Creates a transaction execution from serialized data."""
        return cls(
            id=data["id"],
            name=data["name"],
            module=data["module"],
            parameters=data.get("parameters", {}),
            status=data.get("status", "pending"),
            started_at=data.get("started_at"),
            finished_at=data.get("finished_at"),
            attempts=data.get("attempts", 0),
            exception_type=data.get("exception_type"),
            exception_message=data.get("exception_message"),
            replayable=data.get("replayable", True),
            policy=data.get("policy", TransactionPolicy()),
        )


@dataclass
class ExecutionHistory:
    """
    Represents the complete execution history of an Application.

    The history is independent from the Application execution pool and can be
    serialized to JSON for inspection, persistence, or replay.
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
                transaction.to_dict() for transaction in self.transactions
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

    @classmethod
    def load(
        cls,
        source: str | Path,
    ) -> ExecutionHistory:
        """
        Loads an execution history from a JSON string or file.

        Args:
            source: JSON string or path to a JSON file.

        Returns:
            The loaded execution history.
        """
        source_path = Path(source)

        if source_path.exists():
            data = json.loads(source_path.read_text(encoding="utf-8"))
        else:
            data = json.loads(str(source))

        return cls(
            application=data.get("application"),
            started_at=data.get("started_at"),
            finished_at=data.get("finished_at"),
            status=data.get("status", "pending"),
            transactions=[
                TransactionExecution.from_dict(transaction)
                for transaction in data.get("transactions", [])
            ],
        )


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
        name: str | None = None,
        execution_policy: ApplicationPolicy | None = None,
    ):
        """
        Initializing the application with a driver.

        Args:
            driver (Any): This is the driver of the system being under test.

            report_on_init (str): The message to be reported when the application
             instance is initialized.

            report_on_exit (str): The message to be reported when the application
             instance is destroyed.

            name (str): the name to identify the application in logs.

            policy (TransactionPolicy): the policy to control how the application is executed.
             to be retried.

        Documentation: https://guara.readthedocs.io/en/latest/
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

        self._dry_run = None
        self._disable = None

        if not execution_policy:
            execution_policy = ApplicationPolicy()
        self._policy = execution_policy

    def __del__(self):
        if self._report_on_exit:
            LOGGER.info(self._report_on_exit)

    def _execute_contract(self, kwargs, contract):
        sig = inspect.signature(contract.do)
        valid_keys = sig.parameters.keys()
        filtered_k = {key: value for key, value in kwargs.items() if key in valid_keys}
        Application(self._driver).execute(contract, **filtered_k)

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

        replayable = True
        masked_parameters = {}

        for key, value in parameters.items():
            if self._require_masking(key):
                masked_parameters[key] = SECRET_DEFAULT_VALUE
                continue

            try:
                json.dumps(value)
                masked_parameters[key] = value
            except (TypeError, ValueError):
                masked_parameters[key] = repr(value)
                replayable = False
        execution = TransactionExecution(
            id=uuid.uuid4().hex,
            name=transaction_class.__name__,
            module=_get_module_path(transaction),
            parameters=masked_parameters,
            replayable=replayable,
            policy=self._transaction.execution_policy,
        )

        self._execution_history.add(execution)

        return execution

    def _require_masking(self, key):
        return (
            "secret" in key.lower()
            or "password" in key.lower()
            or "mask" in key.lower()
        )

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

    def replay(
        self,
        history: str | Path | ExecutionHistory,
        parameter_overrides: dict[str, dict[str, Any]] | None = None,
        transaction_id: str | None = None,
        resume: bool = True,
    ) -> Application:
        """
        Replays a previously dumped execution history.

        Transactions are resolved from their recorded module and class name.
        The transactions are executed in the same order in which they were
        originally executed.

        Args:
            history: An ExecutionHistory instance, a JSON string, or a path
                to a dumped execution history.
            parameter_overrides: Optional parameters used to replace masked
                or otherwise unavailable parameters.

                The key is the transaction identifier:

                    {
                        "my_module.CreateOrder": {
                            "customer_id": 10
                        }
                    }

        Returns:
            The current Application instance.

        Raises:
            ReplayError: If a transaction cannot be resolved or its recorded
                parameters cannot safely be replayed.
        """
        if isinstance(history, ExecutionHistory):
            execution_history = history
        else:
            execution_history = ExecutionHistory.load(history)

        if not execution_history.transactions:
            return self

        if transaction_id:
            for index, execution in enumerate(execution_history.transactions):
                if execution.id == transaction_id:
                    if resume:
                        execution_history.transactions = execution_history.transactions[
                            index:
                        ]
                    else:
                        execution_history.transactions = [execution]
                    break
            else:
                raise ReplayError(f"Transaction {transaction_id} not found.")

        parameter_overrides = parameter_overrides or {}

        for transaction_execution in execution_history.transactions:
            if not transaction_execution.replayable:
                raise ReplayError(
                    f"Transaction '{transaction_execution.identifier}' "
                    "cannot be replayed because one or more parameters "
                    "could not be serialized."
                )

            transaction_class = self._resolve_transaction(
                transaction_execution,
            )

            parameters = dict(transaction_execution.parameters)

            overrides = parameter_overrides.get(
                transaction_execution.identifier,
                {},
            )
            parameters.update(overrides)

            masked_parameters = [
                key
                for key, value in parameters.items()
                if value == SECRET_DEFAULT_VALUE
            ]

            if masked_parameters:
                raise ReplayError(
                    f"Transaction '{transaction_execution.identifier}' "
                    f"contains masked parameters that require explicit "
                    f"overrides: {masked_parameters}"
                )

            LOGGER.info(f"Replaying transaction '{transaction_execution.identifier}'.")

            self.at(
                transaction_class,
                **parameters,
            )

        return self

    def _resolve_transaction(
        self,
        transaction_execution: TransactionExecution,
    ) -> type[AbstractTransaction]:
        """
        Resolves a Transaction class from its recorded module and name.
        """
        try:
            module = importlib.import_module(transaction_execution.module)
        except ImportError as exception:
            raise ReplayError(
                f"Unable to import module "
                f"'{transaction_execution.module}' while replaying "
                f"'{transaction_execution.identifier}'."
            ) from exception

        try:
            transaction_class = getattr(
                module,
                transaction_execution.name,
            )
        except AttributeError as exception:
            raise ReplayError(
                f"Unable to find Transaction "
                f"'{transaction_execution.identifier}' while replaying."
            ) from exception

        if not isinstance(transaction_class, type):
            raise ReplayError(f"'{transaction_execution.identifier}' is not a class.")

        if not issubclass(transaction_class, AbstractTransaction):
            raise ReplayError(
                f"'{transaction_execution.identifier}' is not an AbstractTransaction."
            )

        return transaction_class

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
        self._transaction = transaction(self._driver)

        self._dry_run = (
            self._transaction.execution_policy.dry_run
            if self._transaction.execution_policy.dry_run is not None
            else self._policy.dry_run
            if self._policy.dry_run
            else GUARA_DRY_RUN
        )
        if self._dry_run:
            LOGGER.warning("Dry run is enabled. No action will be taken on drivers.")
            if isinstance(
                self._transaction.execution_policy.return_on_dry_run, Exception
            ):
                raise self._transaction.execution_policy.return_on_dry_run
            self._result = self._transaction.execution_policy.return_on_dry_run
            return self

        self._disable = (
            self._transaction.execution_policy.disable
            if self._transaction.execution_policy.disable is not None
            else self._policy.disable
        )

        if self._disable:
            LOGGER.warning(
                f"Transaction '{self._transaction}' disabled. No execution taken."
            )
            return self

        for required in self._transaction.requires:
            self._execute_contract(kwargs, required)

        if any(v for v in self._transaction.execution_policy.to_dict().values()):
            LOGGER.warning(
                f"Policy for transaction '{self._transaction.__name__}': {self._transaction.execution_policy.to_dict()}"
            )

        if self._transaction.execution_policy.retries_on_failure is not None:
            _retries_on_failure = self._transaction.execution_policy.retries_on_failure
        elif self._policy.retries_on_failure is not None:
            _retries_on_failure = self._policy.retries_on_failure
        else:
            _retries_on_failure = GUARA_RETRIES_ON_FAILURE

        self._transaction_pool.append(self._transaction)

        transaction_info: str = get_transaction_info(self._transaction)

        history = self._create_transaction_execution(
            self._transaction,
            kwargs,
            transaction_info,
        )

        history.start()

        masked_parameters = copy.copy(kwargs)
        for key, value in kwargs.items():
            if self._require_masking(key):
                value = SECRET_DEFAULT_VALUE
                masked_parameters[key] = value

        result_details = {
            "transaction": transaction_info,
            "parameters": [{**masked_parameters}],
        }

        exception: Exception = None
        retries: int = 0

        while retries <= _retries_on_failure:
            try:
                retries += 1
                history.attempts = retries

                self._result = self._transaction.act(**kwargs)

                history.succeed(self._result)

                LOGGER.info(f"Transaction '{transaction_info}' succeded.")

                if GUARA_VERBOSE:
                    LOGGER.info(result_details)

                self._execution_history.succeed()

                for ensured in self._transaction.ensures:
                    self._execute_contract(kwargs, ensured)

                return self

            except Exception as e:
                exception = e

                _continue_on_exceptions = (
                    self._transaction.execution_policy.continue_on_exceptions
                    or self._policy.continue_on_exceptions
                    or ()
                )

                if isinstance(e, _continue_on_exceptions):
                    LOGGER.warning(
                        f"Transaction '{transaction.__name__}' continued on Exception ({type(e)})"
                    )
                    return self._result

                _abort_on_exceptions = (
                    self._transaction.execution_policy.abort_on_exceptions
                    or self._policy.abort_on_exceptions
                    or ()
                )
                if isinstance(e, _abort_on_exceptions):
                    LOGGER.error(
                        f"Transaction '{transaction.__name__}' aborted on Exception ({type(e)})"
                    )
                    raise

                _retry_on_exceptions = (
                    self._transaction.execution_policy.retry_on_exceptions
                    or self._policy.retry_on_exceptions
                    or (Exception,)
                )
                if not isinstance(e, _retry_on_exceptions):
                    LOGGER.warning(
                        f"Retry Ignored. Exception ({type(e)})"
                        f" not in retry list ({_retry_on_exceptions})."
                    )
                    break

                LOGGER.error(
                    f"Transaction '{transaction_info}' failed on attempt"
                    f" {retries} / {_retries_on_failure + 1}."
                )
                LOGGER.exception(e)  # noqa

                if self._transaction.execution_policy.pacing_time is not None:
                    _pacing_time = self._transaction.execution_policy.pacing_time
                elif self._policy.pacing_time is not None:
                    _pacing_time = self._policy.pacing_time
                else:
                    _pacing_time = GUARA_PACING_TIME

                if retries <= _retries_on_failure:
                    LOGGER.info(f"Waiting {_pacing_time}s for next retry.")
                    time.sleep(_pacing_time)

        if exception:
            history.fail(exception)

            LOGGER.error(f"Transaction '{transaction_info}' failed.")

            if GUARA_VERBOSE:
                result_details["return"] = f"({type(exception)}) '{exception!s}'"
                LOGGER.error(result_details)

            self._execution_history.fail()
            _rollback = (
                self._transaction.execution_policy.rollback_on_failure
                if self._transaction.execution_policy.rollback_on_failure is not None
                else self._policy.rollback_on_failure
            )
            if _rollback:
                LOGGER.warning(
                    f"Rolling back transaction '{self._transaction.__name__}'."
                )
                self._transaction.undo()
            raise exception

    def given(
        self,
        transaction: AbstractTransaction,
        **kwargs: dict[str, Any],
    ) -> Application:
        """
        Same as the `at` method. Introduced for better readability.

        Performs a transaction.
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
        """
        return self.at(transaction, **kwargs)

    def execute(
        self,
        transaction: AbstractTransaction,
        **kwargs: dict[str, Any],
    ) -> Application:
        """
        Same as the `at` method. Introduced for better readability.
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
        """
        if self._disable:
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
        Asserting and validating the data.
        """
        return self.asserts(assertion, expected)

    def then(
        self,
        assertion: IAssertion,
        expected: Any = None,
    ) -> Application:
        """
        Asserting and validating the data.
        """
        return self.asserts(assertion, expected)

    def undo(self):
        """
        Reverts the actions performed by the `do` method when applicable.

        Returns:
            (Application)
        """
        if self._disable:
            return self

        if self._dry_run:
            return

        self._transaction_pool.reverse()

        for transaction in self._transaction_pool:
            LOGGER.info(f"Reverting transaction '{transaction.__name__}'")
            transaction.revert_action()

        return self
