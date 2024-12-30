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
