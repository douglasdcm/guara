"""
The module that deals with the assertion and validation of a
transaction at the runtime.
"""

from typing import Any, List, Dict
from guara.assertion import IAssertion
from logging import getLogger, Logger
from re import match


LOGGER: Logger = getLogger(__name__)


class IsEqualTo(IAssertion):
    """
    Equality Assertion class
    """
    def asserts(self, actual: Any, expected: Any) -> None:
        assert actual == expected


class IsNotEqualTo(IAssertion):
    """
    Not Equality Assertion class
    """
    def asserts(self, actual: Any, expected: Any) -> None:
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
    The assertion class for verifying that the actual object has
    the expected data.
    """
    def asserts(self, actual: Dict[str, Any], expected: Dict[str, Any]) -> None:
        for key, value in actual.items():
            if list(expected.keys())[0] in key and list(expected.values())[0] in value:
                return
        raise AssertionError("The expected key and value is not in the actual data.")


class MatchesRegex(IAssertion):
    """
    The assertion class for verifying that the actual string
    matches the expected regular expression pattern.
    """
    def asserts(self, actual: str, expected: str) -> None:
        if match(expected, actual):
            return
        raise AssertionError("The actual data does not match the expected regular expression.")


class HasSubset(IAssertion):
    """
    The assertion class for verifying that the expected array is
    a subset of the actual array.
    """
    def asserts(self, actual: List[Any], expected: List[Any]) -> None:
        if set(expected).intersection(actual) == set(expected):
            return
        raise AssertionError("The expected data is not a subset of the actual data.")


class IsSortedAs(IAssertion):
    """
    The assertion class for verifying that that the actual array
    is the expected array.
    """
    def asserts(self, actual: List[Any], expected: List[Any]):
        IsEqualTo().asserts(actual, expected)
