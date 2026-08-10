# Copyright (C) 2025-2026 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://guara.readthedocs.io/en/latest/


from pytest import mark

from guara import it
from guara.asynchronous import it as async_it
from guara.asynchronous.transaction import (
    AbstractTransaction as AsyncAbstractTransaction,
)
from guara.asynchronous.transaction import (
    Application as AsyncApplication,
)
from guara.policy import ExecutionPolicy
from guara.transaction import AbstractTransaction, Application


class MyTransaction(AbstractTransaction):
    def do(self):
        raise PermissionError()


def test_application_do_not_run_when_disabled():
    app = Application(policy=ExecutionPolicy(disable=True))
    (
        app.given(MyTransaction)
        .at(MyTransaction)
        .when(MyTransaction)
        .and_(MyTransaction)
        .so(MyTransaction)
        .execute(MyTransaction)
        .asserts(it.IsEqualTo, "anything")
        .expects(it.IsEqualTo, "anything")
        .then(it.IsEqualTo, "anything")
        .undo()
    )


class MyAsyncTransaction(AsyncAbstractTransaction):
    async def do(self):
        raise PermissionError()


@mark.asyncio
async def test_async_application_do_not_run_when_disabled():
    app = AsyncApplication(disable=True)
    (
        await app.at(MyAsyncTransaction)
        .when(MyAsyncTransaction)
        .and_(MyAsyncTransaction)
        .so(MyAsyncTransaction)
        .asserts(async_it.IsEqualTo, None)
        .then(async_it.IsEqualTo, None)
        .perform()
    )
