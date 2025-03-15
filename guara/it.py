# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

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
    Checks whether the `actual` dictionary has the key and value
    set in `expected`. Returns when the first key-value pair is found and ignores
    the remaining ones.

    Args:
        actual (dict): the dictionary to be inspected
        expected (dict): the key-value pair to be found in `actual`
    """

    def asserts(self, actual: Any, expected: Any) -> None:
        for key, value in actual.items():
            if list(expected.keys())[0] in key and list(expected.values())[0] in value:
                return
        raise AssertionError("The expected key and value is not in the actual data.")


class MatchesRegex(IAssertion):
    """
    Checks whether the `expected` pattern matches the `actual` string

    Args:
        actual (str): the string to be inspected
        expected (str): the pattern to be found in `actual`. For example '(?:anoother){d}'
    """

    def asserts(self, actual: str, expected: str) -> None:
        if match(expected, actual):
            return
        raise AssertionError("The actual data does not match the expected regular expression.")


class HasSubset(IAssertion):
    """
    Checks whether the `expected` list is a subset of `actual`

    Args:
        actual (list): the list to be inspected
        expected (list): the list to be found in `actual`.
    """

    def asserts(self, actual: List[Any], expected: List[Any]) -> None:
        if set(expected).intersection(actual) == set(expected):
            return
        raise AssertionError("The expected data is not a subset of the actual data.")


class IsSortedAs(IAssertion):
    """
    Checks whether the `actual` list is as `expected`

    Args:
        actual (list): the list to be inspected
        expected (list): the ordered list to compare againts `actual`.
    """

    def asserts(self, actual: List[Any], expected: List[Any]):
        IsEqualTo().asserts(actual, expected)
