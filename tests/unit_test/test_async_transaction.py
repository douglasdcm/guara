# Copyright (C) 2025-2026 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

from pytest import mark, raises
from guara.asynchronous.transaction import (
    Application as AsyncApplication,
    AbstractTransaction as AsyncAbstractTransaction,
)


class AsyncMyTransaction(AsyncAbstractTransaction):
    async def do(self, raise_error=False):
        if raise_error:
            raise Exception("Failed")
        return "success"


@mark.asyncio
async def test_async_transaction_raises_error_when_fail():
    with raises(Exception, match="Failed"):
        await AsyncApplication().at(AsyncMyTransaction, raise_error=True).perform()


@mark.asyncio
async def test_async_transaction_succeed():
    app = AsyncApplication()
    await app.at(AsyncMyTransaction).at(AsyncMyTransaction).perform()
    assert app.result == "success"
