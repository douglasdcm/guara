"""
The module that deals with the assertion and validation of a
transaction at the runtime.
"""
from typing import Any
from guara.asynchronous.assertion import IAssertion
from logging import getLogger, Logger


LOGGER: Logger = getLogger("guara")
class IsEqualTo(IAssertion):
    """
    Equality Assertion class
    """
    async def asserts(self, actual: Any, expected: Any) -> None:
        """
        Asserting and validating the data for equality.

        Parameters:
            actual: Any: The actual data to be validated.
            expected: Any: The expected data.

        Returns:
            void
        """
        assert actual.result == expected

class IsNotEqualTo(IAssertion):
    """
    Not Equality Assertion class
    """
    async def asserts(self, actual: Any, expected: Any) -> None:
        """
        Asserting and validating the data for not equality.

        Parameters:
            actual: Any: The actual data to be validated.
            expected: Any: The expected data.

        Returns:
            void
        """
        assert actual.result != expected

class Contains(IAssertion):
    """
    Containing Assertion class
    """
    async def asserts(self, actual: Any, expected: Any) -> None:
        """
        Asserting and validating the data where the expected data is
        in the actual data.

        Parameters:
            actual: Any: The actual data to be validated.
            expected: Any: The expected data.

        Returns:
            void
        """
        assert expected in actual.result

class DoesNotContain(IAssertion):
    """
    Not Containing Assertion class
    """
    async def asserts(self, actual: Any, expected: Any) -> None:
        """
        Asserting and validating the data where the expected data is
        not in the actual data.

        Args:
            actual: (Any): The actual data to be validated.
            expected: (Any): The expected data.

        Returns:
            (None)
        """
        assert expected not in actual.result
