# Copyright (C) 2025-2026 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://guara.readthedocs.io/en/latest/

from pytest import mark, raises

from guara.asynchronous import it
from guara.asynchronous.transaction import (
    AbstractTransaction as AsyncAbstractTransaction,
)
from guara.asynchronous.transaction import (
    Application as AsyncApplication,
)
from guara.policy import TransactionExecutionPolicy


class AsyncMyTransaction(AsyncAbstractTransaction):
    async def do(self):
        return "success"


class AsyncMyFailedTransaction(AsyncAbstractTransaction):
    execution_policy = TransactionExecutionPolicy(
        return_on_dry_run=PermissionError("Failed")
    )

    async def do(self):
        raise PermissionError("Failed")


@mark.asyncio
async def test_async_transaction_raises_error_when_fail():
    with raises(PermissionError, match="Failed"):
        await AsyncApplication().at(AsyncMyFailedTransaction).perform()


@mark.asyncio
async def test_async_transaction_succeed():
    app = AsyncApplication()
    await (
        app.at(AsyncMyTransaction)
        .at(AsyncMyTransaction)
        .asserts(it.IsEqualTo, "success")
        .perform()
    )
