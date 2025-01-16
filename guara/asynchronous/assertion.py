"""
The module that has the interface for the implmentation of
the assertion logic to be used for validation and testing.

Authors:
    douglasdcm
    Darkness4869
"""
from typing import Any, Coroutine
from logging import getLogger, Logger


LOGGER: Logger = getLogger(__name__)
class IAssertion:
    """
    It is the base class for implementing assertion logic which
    is used for validation and testing.
    """
    async def asserts(self, actual: Any, expected: Any) -> None:
        """
        It defines the assertion logic by comparing the actual data
        against the expected data.

        Parameters:
            actual: Any: The actual data
            expected: Any: The expected data

        Returns:
            void
        """
        raise NotImplementedError

    async def validates(self, actual: Any, expected: Any) -> None:
        """
        Executing the assertion logic.

        Parameters:
            actual: Any: The actual data
            expected: Any: The expected data

        Returns:
            void
        """
        try:
            await self.asserts(actual, expected)
        except Exception:
            LOGGER.error(f"actual: {actual.result}")
            LOGGER.error(f"expected: {expected}")
            raise