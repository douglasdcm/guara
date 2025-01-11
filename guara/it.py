from typing import Any


class IAssertion:
    def asserts(self, actual: Any, expected: Any) -> None:
        raise NotImplementedError


class IsEqualTo(IAssertion):
    def asserts(self, actual, expected):
        assert actual == expected


class IsNotEqualTo(IAssertion):
    def asserts(self, actual, expected):
        assert actual != expected


class Contains(IAssertion):
    def asserts(self, actual, expected):
        assert expected in actual


class DoesNotContain(IAssertion):
    def asserts(self, actual, expected):
        assert expected not in actual


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
                return
        raise AssertionError


class MatchesRegex(IAssertion):
    """Checks whether the `expected` pattern matches the `actual` string

    Args:
        actual (str): the string to be inspected
        expected (str): the pattern to be found in `actual`. For example '(?:anoother){d}'
    """

    def asserts(self, actual, expected):
        import re

        if not re.match(expected, actual):
            raise AssertionError


class HasSubset(IAssertion):
    """Checks whether the `expected` list is a subset of `actual`

    Args:
        actual (list): the list to be inspected
        expected (list): the list to be found in `actual`.
    """

    def asserts(self, actual, expected):
        if not set(expected).intersection(actual) == set(expected):
            raise AssertionError


class IsSorted(IAssertion):
    """Checks whether the `actual` list is as `expected`

    Args:
        actual (list): the list to be inspected
        expected (list): the ordenized list to compare againts `actual`.
    """

    def asserts(self, actual, expected):
        IsEqualTo().asserts(actual, expected)
