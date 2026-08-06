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


    _pacing_time = None
    """(int) Local value in seconds to wait between retries.
     Overrides the global variable `GUARA_PACING_TIME`."""

    _retries_on_failure = None
    """(int) Local value to retry failed executions.
     Overrides the global variable `GUARA_RETRIES_ON_FAILURE`."""

    return_on_dry_run = None
    """(Any) Value returned in case dry run is enabled. Prevents break the execution."""

    retry_on_exceptions = None
    """(tuple(Exceptions)) List of exceptions to be retried."""

    def __init__(self, driver: Any = None):
        """
        Initializing the transaction which will allow it to interact
        with the driver.

        Args:
            driver: (Any): It is the driver that controls the user-interface.
        """
        self._driver: Any = driver

    def _handles_integer_variable(self, value):
        try:
            value = int(value)
            if value < 0:
                return
        except Exception: # noqa
            return


    @property
    def retries_on_failure(self):
        return self._handles_integer_variable(self._retries_on_failure)

    @retries_on_failure.setter
    def retries_on_failure(self, value):
        self._retries_on_failure = value

    @property
    def pacing_time(self):
        return self._handles_integer_variable(self._pacing_time)

    @pacing_time.setter
    def pacing_time(self, value):
        self._pacing_time = value



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
