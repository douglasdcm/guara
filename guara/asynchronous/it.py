# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

"""
The module that deals with the assertion and validation of a
transaction at the runtime.
"""

from typing import Any
from guara.asynchronous.assertion import IAssertion
from logging import getLogger, Logger


LOGGER: Logger = getLogger("guara")


class IsEqualTo(IAssertion):
    """
    Equality Assertion class
    """

    async def asserts(self, actual: Any, expected: Any) -> None:
        assert actual.result == expected


class IsNotEqualTo(IAssertion):
    """
    Not Equality Assertion class
    """

    async def asserts(self, actual: Any, expected: Any) -> None:
        assert actual.result != expected


class Contains(IAssertion):
    """
    Containing Assertion class
    """

    async def asserts(self, actual: Any, expected: Any) -> None:
        assert expected in actual.result


class DoesNotContain(IAssertion):
    """
    Not Containing Assertion class
    """

    async def asserts(self, actual: Any, expected: Any) -> None:
        assert expected not in actual.result
