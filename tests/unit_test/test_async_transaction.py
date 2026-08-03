# Copyright (C) 2025-2026 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

from pytest import mark, raises
from guara.asynchronous import it
from guara.asynchronous.transaction import (
    Application as AsyncApplication,
    AbstractTransaction as AsyncAbstractTransaction,
)


class AsyncMyTransaction(AsyncAbstractTransaction):
    async def do(self):
        return "success"


class AsyncMyFailedTransaction(AsyncAbstractTransaction):
    return_on_dry_run = Exception("Failed")

    async def do(self):
        raise Exception("Failed")


@mark.asyncio
async def test_async_transaction_raises_error_when_fail():
    with raises(Exception, match="Failed"):
        await AsyncApplication().at(AsyncMyFailedTransaction).perform()


@mark.asyncio
async def test_async_transaction_succeed():
    app = AsyncApplication()
    await app.at(AsyncMyTransaction).at(AsyncMyTransaction).asserts(
        it.IsEqualTo, "success"
    ).perform()
