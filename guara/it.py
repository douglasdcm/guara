import logging
from typing import Any

LOGGER = logging.getLogger(__name__)


class IAssertion:
    def asserts(self, actual: Any, expected: Any) -> bool | AssertionError:
        raise NotImplementedError

    def validates(self, actual, expected):
        LOGGER.info(f"Assertion '{self.__class__.__name__}'")
        try:
            result = self.asserts(actual, expected)
            LOGGER.info(f" actual:   '{actual}'")
            LOGGER.info(f" expected: '{expected}'")
            return result
        except Exception:
            LOGGER.error(f" actual:   '{actual}'")
            LOGGER.error(f" expected: '{expected}'")
            raise


class IsEqualTo(IAssertion):
    def asserts(self, actual, expected):
        if actual == expected:
            return True
        raise AssertionError


class IsNotEqualTo(IAssertion):
    def asserts(self, actual, expected):
        if actual != expected:
            return True
        raise AssertionError


class Contains(IAssertion):
    def asserts(self, actual, expected):
        if expected in actual:
            return True
        raise AssertionError


class DoesNotContain(IAssertion):
    def asserts(self, actual, expected):
        if expected not in actual:
            return True
        raise AssertionError


class HasKeyValue(IAssertion):
    """Checks whether the `actual` dictionary has the key and value
    set in `expected`. Returns when the first key-value pair is found and ignores
    the remaining ones.

    Args:
        actual (dict): the dictionary to be inspected
        expected (dict): the key-value pair to be found in `actual`
    """

    def asserts(self, actual, expected):
        for k, v in actual.items():
            if list(expected.keys())[0] in k and list(expected.values())[0] in v:
                return True
        raise AssertionError


class MatchesRegex(IAssertion):
    """Checks whether the `expected` pattern matches the `actual` string

    Args:
        actual (str): the string to be inspected
        expected (str): the pattern to be found in `actual`. For example '(?:anoother){d}'
    """

    def asserts(self, actual, expected):
        import re

        if re.match(expected, actual):
            return True
        raise AssertionError


class HasSubset(IAssertion):
    """Checks whether the `expected` list is a subset of `actual`

    Args:
        actual (list): the list to be inspected
        expected (list): the list to be found in `actual`.
    """

    def asserts(self, actual, expected):
        if set(expected).intersection(actual) == set(expected):
            return True
        raise AssertionError


class IsSortedAs(IAssertion):
    """Checks whether the `actual` list is as `expected`

    Args:
        actual (list): the list to be inspected
        expected (list): the ordered list to compare againts `actual`.
    """

    def asserts(self, actual, expected):
        return IsEqualTo().asserts(actual, expected)
