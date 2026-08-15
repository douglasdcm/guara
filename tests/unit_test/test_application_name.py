# Copyright (C) 2025-2026 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://guara.readthedocs.io/en/latest/


from pytest import mark

from guara.asynchronous.transaction import (
    Application as AsyncApplication,
)
from guara.transaction import Application


def test_application_logs_name_when_name_is_filled(caplog):
    Application(name="My app")
    assert "My app" in caplog.text


@mark.asyncio
async def test_async_application_logs_name_when_name_is_filled(caplog):
    AsyncApplication(name="My app")
    assert "My app" in caplog.text
