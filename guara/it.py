"""
The module that deals with the assertion and validation of a
transaction at the runtime.

Authors:
    douglasdcm
    RonaldTheodoro
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
    def asserts(self, actual, expected) -> None:
        """
        Asserting and validating the data where the expected data is
        in the actual data.

        Parameters:
            actual: Any: The actual data to be validated.
            expected: Any: The expected data.

        Returns:
            void
        """
        assert expected in actual

class DoesNotContain(IAssertion):
    """
    Not Containing Assertion class
    """
    def asserts(self, actual: Any, expected: Any) -> None:
        """
        Asserting and validating the data where the expected data is
        not in the actual data.

        Parameters:
            actual: Any: The actual data to be validated.
            expected: Any: The expected data.

        Returns:
            void
        """
        assert expected not in actual

class HasKeyValue(IAssertion):
    """
    Key-Value Assertion class
    """
    def asserts(self, actual: Any, expected: Any) -> None:
        """
        Asserting and validating the data where the expected data is
        in the object of the actual data.

        Parameters:
            actual: Any: The actual data to be validated.
            expected: Any: The expected data.

        Returns:
            void
        """
        for key, value in actual.items():
            if list(expected.keys())[0] in key and list(expected.values())[0] in value:
                return
        raise AssertionError

class MatchesRegex(IAssertion):
    """
    Regular Expression Matches Assertion class
    """
    def asserts(self, actual: str, expected: str) -> None:
        """
        Asserting and validating the data where the expected data is
        not in the actual data.

        Parameters:
            actual: string: The actual data to be validated.
            expected: string: The regex pattern

        Returns:
            void
        """
        if match(expected, actual):
            return
        raise AssertionError

class HasSubset(IAssertion):
    """
    Has Subset Assertion class
    """
    def asserts(self, actual: List[Any], expected: List[Any]) -> None:
        """
        Asserting and validating the data where the expected data is
        a subset of the actual data.

        Parameters:
            actual: [Any]: The actual data to be validated.
            expected: [Any]: The expected data to be found in the actual data.

        Returns:
            void
        """
        if set(expected).intersection(actual) == set(expected):
            return
        raise AssertionError

class IsSortedAs(IAssertion):
    """
    Sorted As Assertion class
    """
    def asserts(self, actual: List[Any], expected: List[Any]):
        """
        Asserting and validating the data where the expected data is
        a subset of the actual data.

        Parameters:
            actual: [Any]: The actual data to be validated.
            expected: [Any]: The expected data to be found in the actual data.

        Returns:
            void
        """
        IsEqualTo().asserts(actual, expected)
