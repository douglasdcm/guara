from unittest.mock import patch

from pytest import mark
from guara import it
from guara.transaction import Application, AbstractTransaction
from guara.asynchronous import it as async_it
from guara.asynchronous.transaction import (
    Application as AsyncApplication,
    AbstractTransaction as AsyncAbstractTransaction,
)


class MyTransaction(AbstractTransaction):
    def do(self):
        return "success"


@patch("guara.abstract_transaction.GUARA_DRY_RUN", True)
@patch("guara.transaction.GUARA_DRY_RUN", True)
def test_transaction_is_not_executed_when_dry_run_is_true():
    app = Application()
    app.at(MyTransaction).asserts(it.IsNone)


@patch("guara.assertion.GUARA_DRY_RUN", True)
def test_assertion_is_not_executed_when_dry_run_is_true():
    app = Application()
    app.at(MyTransaction).asserts(it.IsEqualTo, "wrong-value")


class MyAsyncTransaction(AsyncAbstractTransaction):
    async def do(self):
        return "success"


@mark.asyncio
@patch("guara.asynchronous.transaction.GUARA_DRY_RUN", True)
async def test_async_transaction_is_not_executed_when_dry_run_is_true():
    app = AsyncApplication()
    await app.at(MyAsyncTransaction).asserts(async_it.IsEqualTo, None).perform()


@mark.asyncio
@patch("guara.asynchronous.assertion.GUARA_DRY_RUN", True)
async def test_async_assertion_is_not_executed_when_dry_run_is_true():
    app = AsyncApplication()
    await app.at(MyAsyncTransaction).asserts(async_it.IsEqualTo, "wrong-vallue").perform()
