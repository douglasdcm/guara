# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

"""
The module that has the interface for the implmentation of
the assertion logic to be used for validation and testing.
"""

from typing import Any
from logging import getLogger, Logger


LOGGER: Logger = getLogger(__name__)


class IAssertion:
    """
    It is the base class for implementing assertion logic which
    is used for validation and testing.
    """

    @property
    def __name__(self) -> property:
        """
        The name of the assertion

        Returns:
            (str) The name of the assertion being implemented.
        """
        return self.__class__.__name__

    async def asserts(self, actual: Any, expected: Any) -> None:
        """
        It defines the assertion logic by comparing the actual data
        against the expected data.

        Args:
            actual: (Any): The actual data
            expected: (Any): The expected data

        Returns:
            (None)

        Raises:
            NotImplementedError: The method is not implemented in the subclass.
        """
        raise NotImplementedError

    async def validates(self, actual: Any, expected: Any) -> None:
        """
        Executing the assertion logic.

        Args:
            actual: (Any): The actual data
            expected: (Any): The expected data

        Returns:
            (None)
        """
        try:
            await self.asserts(actual, expected)
        except Exception as e:
            LOGGER.error(f" Actual  : {actual.result}")
            LOGGER.error(f" Expected: {expected}")
            LOGGER.exception(str(e))
            raise
