# Copyright (C) 2025-2026 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://guara.readthedocs.io/en/latest/

import logging

from pytest import mark

from guara.asynchronous.transaction import (
    AbstractTransaction as AsyncAbstractTransaction,
)
from guara.asynchronous.transaction import (
    Application as AsyncApplication,
)
from guara.transaction import AbstractTransaction, Application


class MyTransaction(AbstractTransaction):
    def do(self):
        return "success"


def test_reports_message_when_application_starts(caplog):
    caplog.set_level(logging.INFO)
    expected = "Application starts"
    Application(report_on_init=expected).at(MyTransaction).at(MyTransaction)
    assert expected in caplog.text


def test_reports_message_when_application_finishes(caplog):
    caplog.set_level(logging.INFO)
    expected = "Application finished"
    Application(report_on_exit=expected).at(MyTransaction).at(MyTransaction)
    assert expected in caplog.text


class AsyncMyTransaction(AsyncAbstractTransaction):
    async def do(self):
        return "success"


@mark.asyncio
async def test_async_reports_message_when_application_starts(caplog):
    caplog.set_level(logging.INFO)
    expected = "Application starts"
    await (
        AsyncApplication(report_on_init=expected)
        .at(AsyncMyTransaction)
        .at(AsyncMyTransaction)
        .perform()
    )
    assert expected in caplog.text


@mark.asyncio
async def test_async_reports_message_when_application_finishes(caplog):
    caplog.set_level(logging.INFO)
    expected = "Application finished"
    await (
        AsyncApplication(report_on_exit=expected)
        .at(AsyncMyTransaction)
        .at(AsyncMyTransaction)
        .perform()
    )
    assert expected in caplog.text
