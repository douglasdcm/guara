import logging
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from guara.asynchronous.transaction import AbstractTransaction

LOGGER = logging.getLogger("guara")


class IAssertion:

    async def asserts(self, actual: "AbstractTransaction", expected: Any) -> None:
        raise NotImplementedError

    async def validates(self, actual, expected):
        try:
            await self.asserts(actual, expected)
        except Exception:
            LOGGER.error(f"actual:   '{actual.result}'")
            LOGGER.error(f"expected: '{expected}'")
            raise


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
