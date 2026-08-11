# Copyright (C) 2025-2026 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://guara.readthedocs.io/en/latest/

"""
It is the module where Policies are implemented.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from logging import Logger, getLogger
from typing import Any

LOGGER: Logger = getLogger(__name__)


@dataclass
class ApplicationExecutionPolicy:
    retry_on_exceptions: tuple[type[Exception], ...] | None = None
    """(tuple(Exceptions)) Tuple of exceptions to be retried."""

    abort_on_exceptions: tuple[type[Exception], ...] | None = None
    """(tuple(Exceptions)) Tuple of exceptions that abort the execution."""

    continue_on_exceptions: tuple[type[Exception], ...] | None = None
    """(tuple(Exceptions)) Tuple of exceptions to be ignored."""

    rollback_on_failure: bool | None = None
    """(bool) Wheter the automatic rollbacks of the transactions are executed."""

    disable: bool | None = None
    """(bool) Wheter the executions of the application is disabled."""

    dry_run: bool | None = None
    """(bool) Wheter the executions of the application hits the driver (False) or not (True)."""

    def __post_init__(self):
        """Validates the class attributes assigned in the subclass."""
        self._validate_continue_on_exceptions()
        self._validate_abort_on_exceptions()
        self._validate_retry_on_exceptions()
        self._validate_rollback_on_failure()
        self._validate_disable()
        self._validate_dry_run()

    @property
    def __name__(self) -> property:
        """
        The name of the policy

        Returns:
            (str) The name of the policy being implemented.
        """
        return self.__class__.__name__

    def _validate_dry_run(self):
        if self.dry_run is None:
            return

        if isinstance(self.dry_run, bool):
            return

        LOGGER.warning(
            f"Invalid value in 'dry_run' in policy '{self.__name__}'."
            " Resetting to 'None'."
        )
        self.dry_run = None

    def _validate_disable(self):
        if self.disable is None:
            return

        if isinstance(self.disable, bool):
            return

        LOGGER.warning(
            f"Invalid value in 'disable' in policy '{self.__name__}'."
            " Resetting to 'None'."
        )
        self.disable = None

    def _validate_rollback_on_failure(self):
        if self.rollback_on_failure is None:
            return

        if isinstance(self.rollback_on_failure, bool):
            return

        LOGGER.warning(
            f"Invalid value in 'rollback_on_failure' in policy '{self.__name__}'."
            " Resetting to 'None'."
        )
        self.rollback_on_failure = None

    def _validate_continue_on_exceptions(self):
        if self.continue_on_exceptions is None:
            return

        message = (
            f"Invalid value in 'continue_on_exceptions' in policy '{self.__name__}'."
            " Resetting to 'None'."
        )

        if not isinstance(self.continue_on_exceptions, tuple):
            LOGGER.warning(message)
            self.continue_on_exceptions = None
            return

        try:
            if not all(isinstance(e(), Exception) for e in self.continue_on_exceptions):
                LOGGER.warning(message)
                self.continue_on_exceptions = None
        except TypeError:
            self.continue_on_exceptions = None

    def _validate_abort_on_exceptions(self):
        if self.abort_on_exceptions is None:
            return

        message = (
            f"Invalid value in 'abort_on_exceptions' in policy '{self.__name__}'."
            " Resetting to 'None'."
        )

        if not isinstance(self.abort_on_exceptions, tuple):
            LOGGER.warning(message)
            self.abort_on_exceptions = None
            return

        try:
            if not all(isinstance(e(), Exception) for e in self.abort_on_exceptions):
                LOGGER.warning(message)
                self.abort_on_exceptions = None
        except TypeError:
            self.abort_on_exceptions = None

    def _validate_retry_on_exceptions(self):
        if self.retry_on_exceptions is None:
            return

        message = (
            f"Invalid value in 'retry_on_exceptions' in policy '{self.__name__}'."
            " Resetting to 'None'."
        )

        if not isinstance(self.retry_on_exceptions, tuple):
            LOGGER.warning(message)
            self.retry_on_exceptions = None
            return

        try:
            if not all(isinstance(e(), Exception) for e in self.retry_on_exceptions):
                LOGGER.warning(message)
                self.retry_on_exceptions = None
        except TypeError:
            self.retry_on_exceptions = None

    def to_dict(self) -> dict[str, Any]:
        """Returns the transaction execution as a dictionary."""
        return asdict(self)


@dataclass
class TransactionExecutionPolicy(ApplicationExecutionPolicy):
    pacing_time: int | None = None
    """(int) Local value in seconds to wait between retries.
     Overrides the global variable `GUARA_PACING_TIME`."""

    retries_on_failure: int | None = None
    """(int) Local value to retry failed executions. Need to be a positive integer.
     Overrides the global variable `GUARA_RETRIES_ON_FAILURE`."""

    return_on_dry_run: Any | None = None
    """(Any) Value returned in case dry run is enabled. Prevents break the execution."""

    def __post_init__(self):
        """Validates the class attributes assigned in the subclass."""
        super().__post_init__()
        self._validate_pacing_time()
        self._validate_retries_on_failure()

    @property
    def __name__(self) -> property:
        """
        The name of the policy

        Returns:
            (str) The name of the policy being implemented.
        """
        return self.__class__.__name__

    def _validate_disable(self):
        if self.disable is None:
            return

        if isinstance(self.disable, bool):
            return

        LOGGER.warning(
            f"Invalid value in 'disable' in policy '{self.__name__}'."
            " Resetting to 'None'."
        )
        self.disable = None

    def _validate_rollback_on_failure(self):
        if self.rollback_on_failure is None:
            return

        if isinstance(self.rollback_on_failure, bool):
            return

        LOGGER.warning(
            f"Invalid value in 'rollback_on_failure' in policy '{self.__name__}'."
            " Resetting to 'None'."
        )
        self.rollback_on_failure = None

    def _validate_retries_on_failure(self):
        if self.retries_on_failure is None:
            return

        if isinstance(self.retries_on_failure, int) and self.retries_on_failure >= 0:
            return

        LOGGER.warning(
            f"Invalid value in 'retries_on_failure' in policy '{self.__name__}'."
            " Resetting to 'None'."
        )
        self.retries_on_failure = None

    def _validate_pacing_time(self):
        if self.pacing_time is None:
            return

        if isinstance(self.pacing_time, int) and self.pacing_time >= 0:
            return

        LOGGER.warning(
            f"Invalid value of 'pacing_time' in policy '{self.__name__}'."
            " Resetting to 'None'."
        )
        self.pacing_time = None

    def to_dict(self) -> dict[str, Any]:
        """Returns the transaction execution as a dictionary."""
        return asdict(self)
