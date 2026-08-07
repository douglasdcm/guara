# Copyright (C) 2025-2026 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

"""
It is the module where the AbstractTransaction will handle
web transactions in an automated browser.
"""
from __future__ import annotations

from logging import Logger, getLogger
from typing import Any, NoReturn

from guara.constants import GUARA_DRY_RUN

LOGGER: Logger = getLogger(__name__)


class AbstractTransaction:
    """
    Manages transaction execution by leveraging an injected driver.
    The driver can be any external dependency, such as a webdriver,
    database instance, or custom object.
    """

    pacing_time : int | None = None
    """(int) Local value in seconds to wait between retries.
     Overrides the global variable `GUARA_PACING_TIME`."""

    retries_on_failure : int | None = None
    """(int) Local value to retry failed executions. Need to be a positive integer.
     Overrides the global variable `GUARA_RETRIES_ON_FAILURE`."""

    return_on_dry_run : Any | None = None
    """(Any) Value returned in case dry run is enabled. Prevents break the execution."""

    retry_on_exceptions : tuple[Exception] | None = None
    """(tuple(Exceptions)) Tuple of exceptions to be retried."""

    def __new__(cls, *args, **kwargs):
        cls._validate_class_variables()
        return super().__new__(cls)

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

    @classmethod
    def _validate_class_variables(cls):
        """Validates the class attributes assigned in the subclass."""
        cls._validate_pacing_time()
        cls._validate_retries_on_failure()
        cls._validate_retry_on_eceptions()

    @classmethod
    def _validate_retry_on_eceptions(cls):
        if cls.retry_on_exceptions is None:
            return
        
        message = (
                f"Invalid value in 'retry_on_exceptions' in transaction '{cls.__name__}'."
                " Resetting to 'None'."
            )

        if not isinstance(cls.retry_on_exceptions, tuple):
            LOGGER.warning(message)
            cls.retry_on_exceptions = None
            return
        if not all(isinstance(e(), Exception) for e in cls.retry_on_exceptions):
            LOGGER.warning(message)
            cls.retry_on_exceptions = None
            return

    @classmethod
    def _validate_retries_on_failure(cls):
        if cls.retries_on_failure is None:
            return

        if not isinstance(cls.retries_on_failure, int) or cls.retries_on_failure < 0:
            LOGGER.warning(
                f"Invalid value in 'retries_on_failure' in transaction '{cls.__name__}'."
                " Resetting to 'None'."
            )
            cls.retries_on_failure = None

    @classmethod
    def _validate_pacing_time(cls):
        if cls.pacing_time is None:
            return

        if not isinstance(cls.pacing_time, int) or cls.pacing_time < 0:
            LOGGER.warning(
                f"Invalid value of 'pacing_time' in transaction '{cls.__name__}'."
                " Resetting to 'None'."
            ) 
            cls.pacing_time = None

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
            if isinstance(self.return_on_dry_run, Exception):
                raise self.return_on_dry_run
            return self.return_on_dry_run
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
