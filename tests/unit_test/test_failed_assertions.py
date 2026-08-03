# Copyright (C) 2026 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

from guara import it
from guara.asynchronous import it as async_it
import pytest
from guara.transaction import Application, AbstractTransaction
from guara.asynchronous.transaction import (
    Application as AsyncApp,
    AbstractTransaction as AsyncTransaction,
)


class ReturnWrongResult(AbstractTransaction):
    def do(self):
        return "wrong"


class TestFailedAssertions:
    @pytest.fixture(autouse=True, scope="function")
    def setup_method(self):
        self._app = Application()

    def test_raise_exception_when_assertion_fails(self):
        expected = "right"
        with pytest.raises(AssertionError):
            self._app.at(ReturnWrongResult).asserts(it.IsEqualTo, expected)


class AsyncReturnWrongResult(AsyncTransaction):
    async def do(self):
        return "wrong"


class TestAsyncFailedAssertions:
    @pytest.mark.asyncio
    async def test_async_raises_exception_when_assertion_fails(self):
        expected = "right"
        app = AsyncApp()
        with pytest.raises(AssertionError):
            await app.at(AsyncReturnWrongResult).asserts(async_it.IsEqualTo, expected).perform()
