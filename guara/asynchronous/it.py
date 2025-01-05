from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from guara.asynchronous.transaction import AbstractTransaction


class IAssertion:
    async def asserts(self, actual: "AbstractTransaction", expected: Any) -> None:
        raise NotImplementedError


class IsEqualTo(IAssertion):
    async def asserts(self, actual, expected):
        assert actual.result == expected


class IsNotEqualTo(IAssertion):
    async def asserts(self, actual, expected):
        assert actual.result != expected


class Contains(IAssertion):
    async def asserts(self, actual, expected):
        assert expected.result in actual


class DoesNotContain(IAssertion):
    async def asserts(self, actual, expected):
        assert expected.result not in actual
