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

    def asserts(self, actual: Any, expected: Any) -> None:
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

    def validates(self, actual: Any, expected: Any) -> None:
        """
        Executing the assertion logic.

        Args:
            actual: (Any): The actual data
            expected: (Any): The expected data

        Returns:
            (None)

        Raises:
            Exception: An assertion exception
        """
        LOGGER.info(f"Assertion: {self.__class__.__name__}")
        try:
            self.asserts(actual, expected)
            LOGGER.info(f" Actual Data: {actual}")
            LOGGER.info(f" Expected: {expected}")
        except Exception:
            LOGGER.error(f" Actual Data: {actual}")
            LOGGER.error(f" Expected: {expected}")
            raise Exception(
                f"The data failed the validation!\nActual Data: {actual}\nExpected Data: {expected}"
            )
