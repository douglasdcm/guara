# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

"""
The module that deals with the assertion and validation of a
transaction at the runtime.
"""

from guara.assertion import IAssertion
from logging import getLogger, Logger


LOGGER: Logger = getLogger(__name__)


class IsEqualTo(IAssertion):
    """
    Asserts that the actual is equal to the expected value.

    Args:
        actual (Any): the first item to compare
        expected (Any): the second item to compare against the first one
    """

    def asserts(self, actual, expected):
        assert actual == expected, f"Expected '{expected}' but got '{actual}'"


class IsNotEqualTo(IAssertion):
    """
    Asserts that the actual is not equal to the expected value.

    Args:
        actual (Any): the first item to compare
        expected (Any): the second item to compare against the first one
    """

    def asserts(self, actual, expected):
        assert actual != expected, f"Did not expect '{expected}'"


class IsTrue(IAssertion):
    """
    Asserts that the actual evaluates to True.

    Args:
        actual (Any): the item to compare validate if it is True
    """

    def asserts(self, actual, expected=None):
        assert bool(actual) is True, f"Expected True but got '{actual}'"


class IsFalse(IAssertion):
    """
    Asserts that the actual evaluates to False.

    Args:
        actual (Any): the item to validate it is False
    """

    def asserts(self, actual, expected=None):
        assert bool(actual) is False, f"Expected False but got '{actual}'"


class IsNone(IAssertion):
    """
    Asserts that the actual is None.

    Args:
        actual (Any): the item to validate if it is `None`
    """

    def asserts(self, actual, expected=None):
        assert actual is None, f"Expected None but got '{actual}'"


class IsNotNone(IAssertion):
    """
    Asserts that the actual is not None.

    Args:
        actual (Any): the item to validate if it is not `None`
    """

    def asserts(self, actual, expected=None):
        assert actual is not None, "Expected value not to be None"


class IsEmpty(IAssertion):
    """
    Asserts that the actual is an empty collection.

    Args:
        actual (Any): the item to validate if it is empty
    """

    def asserts(self, actual, expected=None):
        assert len(actual) == 0, f"Expected empty but got '{actual}'"


class IsNotEmpty(IAssertion):
    """
    Asserts that the actual is not an empty collection.

    Args:
        actual (Any): the item to validate if it is not empty
    """

    def asserts(self, actual, expected=None):
        assert len(actual) > 0, "Expected non-empty collection"


class HasLength(IAssertion):
    """
    Asserts that the actual has the expected length.

    Args:
        actual (Any): the item to check the length
        expected (int): the expected length of the item
    """

    def asserts(self, actual, expected):
        assert len(actual) == expected, f"Expected length {expected} but got {len(actual)}"


class Contains(IAssertion):
    """
    Asserts that the expected value is contained in the actual.

    Args:
        actual (Any): the item to check if contains the expected ones
        expected (Any): the expected items in `actual`
    """

    def asserts(self, actual, expected):
        assert expected in actual, f"Expected '{expected}' to be in '{actual}'"


class DoesNotContain(IAssertion):
    """
    Asserts that the expected value is not contained in the actual.
    """

    def asserts(self, actual, expected):
        assert expected not in actual, f"Did not expect '{expected}' in '{actual}'"


class ContainsAll(IAssertion):
    """
    Asserts that all expected values are present in the actual.
    """

    def asserts(self, actual, expected):
        missing = [item for item in expected if item not in actual]
        assert not missing, f"Missing items: {missing}"


class ContainsAny(IAssertion):
    """
    Asserts that at least one of the expected values is present in the actual.
    """

    def asserts(self, actual, expected):
        assert any(item in actual for item in expected), f"None of {expected} found in {actual}"


class IsGreaterThan(IAssertion):
    """
    Asserts that the actual is greater than the expected value.
    """

    def asserts(self, actual, expected):
        assert actual > expected, f"Expected > {expected} but got {actual}"


class IsLessThan(IAssertion):
    """
    Asserts that the actual is less than the expected value.
    """

    def asserts(self, actual, expected):
        assert actual < expected, f"Expected < {expected} but got {actual}"


class IsBetween(IAssertion):
    """
    Asserts that the actual is between two values (inclusive).
    """

    def asserts(self, actual, expected):
        low, high = expected
        assert low <= actual <= high, f"Expected between {low} and {high} but got {actual}"


class IsCloseTo(IAssertion):
    """
    Asserts that the actual is within a tolerance of a target value.
    """

    def asserts(self, actual, expected):
        value, tolerance = expected
        assert abs(actual - value) <= tolerance, f"{actual} not within {tolerance} of {value}"


class StartsWith(IAssertion):
    """
    Asserts that the actual starts with the expected prefix.
    """

    def asserts(self, actual, expected):
        assert str(actual).startswith(expected), f"'{actual}' does not start with '{expected}'"


class EndsWith(IAssertion):
    """
    Asserts that the actual ends with the expected suffix.
    """

    def asserts(self, actual, expected):
        assert str(actual).endswith(expected), f"'{actual}' does not end with '{expected}'"


class MatchesRegex(IAssertion):
    """
    Asserts that the actual matches the given regular expression.
    """

    def asserts(self, actual, expected):
        import re

        assert re.search(expected, str(actual)), f"'{actual}' does not match regex '{expected}'"


class IsBlank(IAssertion):
    """
    Asserts that the actual is an empty or whitespace-only string.
    """

    def asserts(self, actual, expected=None):
        assert str(actual).strip() == "", f"Expected blank but got '{actual}'"


class IsNotBlank(IAssertion):
    """
    Asserts that the actual is not an empty or whitespace-only string.
    """

    def asserts(self, actual, expected=None):
        assert str(actual).strip() != "", "Expected non-blank string"


class HasChanged(IAssertion):
    """
    Asserts that the actual is different from the previous value.
    """

    def asserts(self, actual, expected):
        previous = expected
        assert actual != previous, f"Value did not change from '{previous}'"


class HasNotChanged(IAssertion):
    """
    Asserts that the actual is equal to the previous value.
    """

    def asserts(self, actual, expected):
        previous = expected
        assert actual == previous, f"Value changed from '{previous}' to '{actual}'"


class Satisfies(IAssertion):
    """
    Asserts that the actual satisfies a custom condition function.
    """

    def asserts(self, actual, expected):
        assert callable(expected), "Expected must be a function"
        assert expected(actual), f"Condition not satisfied for '{actual}'"


class HasSubset(IAssertion):
    """
    Checks whether the `expected` list is a subset of `actual`

    Args:
        actual (list): the list to be inspected
        expected (list): the list to be found in `actual`.
    """

    def asserts(self, actual, expected) -> None:
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

    def asserts(self, actual, expected):
        IsEqualTo().asserts(actual, expected)


class HasKeyValue(IAssertion):
    """
    Checks whether the `actual` dictionary has the key and value
    set in `expected`. Returns when the first key-value pair is found and ignores
    the remaining ones.

    Args:
        actual (dict): the dictionary to be inspected
        expected (dict): the key-value pair to be found in `actual`
    """

    def asserts(self, actual, expected) -> None:
        for key, value in actual.items():
            if list(expected.keys())[0] in key and list(expected.values())[0] in value:
                return
        raise AssertionError("The expected key and value is not in the actual data.")
