"""
The module that deals with the assertion and validation of a
transaction at the runtime.
"""
from typing import Any, List
from guara.assertion import IAssertion
from logging import getLogger, Logger
from re import match


LOGGER: Logger = getLogger(__name__)
class IsEqualTo(IAssertion):
    """
    Equality Assertion class
    """
    def asserts(self, actual: Any, expected: Any) -> None:
        """
        Asserting and validating the data for equality.

        Parameters:
            actual: Any: The actual data to be validated.
            expected: Any: The expected data.

        Returns:
            void
        """
        assert actual == expected

class IsNotEqualTo(IAssertion):
    """
    Not Equality Assertion class
    """
    def asserts(self, actual: Any, expected: Any) -> None:
        """
        Asserting and validating the data for not equality.

        Parameters:
            actual: Any: The actual data to be validated.
            expected: Any: The expected data.

        Returns:
            void
        """
        assert actual != expected

class Contains(IAssertion):
    """
    Containing Assertion class
    """
    def asserts(self, actual: Any, expected: Any) -> None:
        assert expected in actual

class DoesNotContain(IAssertion):
    """
    Not Containing Assertion class
    """
    def asserts(self, actual: Any, expected: Any) -> None:
        assert expected not in actual

class HasKeyValue(IAssertion):
    """
    Key-Value Assertion class
    """
    def asserts(self, actual: Any, expected: Any) -> None:
        for key, value in actual.items():
            if list(expected.keys())[0] in key and list(expected.values())[0] in value:
                return
        raise AssertionError("The expected key and value is not in the actual data.")

class MatchesRegex(IAssertion):
    """
    Regular Expression Matches Assertion class
    """
    def asserts(self, actual: str, expected: str) -> None:
        if match(expected, actual):
            return
        raise AssertionError("The actual data does not match the expected regular expression.")

class HasSubset(IAssertion):
    """
    Has Subset Assertion class
    """
    def asserts(self, actual: List[Any], expected: List[Any]) -> None:
        if set(expected).intersection(actual) == set(expected):
            return
        raise AssertionError("The expected data is not a subset of the actual data.")

class IsSortedAs(IAssertion):
    """
    Sorted As Assertion class
    """
    def asserts(self, actual: List[Any], expected: List[Any]):
        IsEqualTo().asserts(actual, expected)
