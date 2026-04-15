# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

import logging
import pytest
from guara.transaction import Application, AbstractTransaction
from guara.asynchronous.transaction import (
    Application as AsyncApp,
    AbstractTransaction as AsyncTransaction,
)


class DoNothing(AbstractTransaction):
    def do(self, any_param=None, my_secret_parameter=None):
        return


class TestHideSecret:
    @pytest.fixture(autouse=True, scope="function")
    def setup_method(self):
        self._app = Application()

    def test_dont_hide_when_parameter_is_not_secret(self, caplog):
        caplog.set_level(logging.INFO)
        expected = "any"
        self._app.at(DoNothing, any_param=expected)
        assert expected in caplog.text

    def test_hide_when_parameter_is_secret(self, caplog):
        caplog.set_level(logging.INFO)
        expected = "***"
        self._app.at(DoNothing, my_secret_parameter="foo")
        assert expected in caplog.text


class AsyncDoNothing(AsyncTransaction):
    async def do(self, any_param=None, my_secret_parameter=None):
        return


class TestAsyncHideSecret:
    @pytest.mark.asyncio
    async def test_async_dont_hide_when_parameter_is_not_secret(self, caplog):
        caplog.set_level(logging.INFO)
        value = "buyCheese@"
        expected = value
        app = AsyncApp()
        await app.at(AsyncDoNothing, any_param=value).perform()
        assert expected in caplog.text

    @pytest.mark.asyncio
    async def test_async_hide_when_parameter_is_secret(self, caplog):
        app = AsyncApp()
        caplog.set_level(logging.INFO)
        value = "buyCheese@"
        expected = "****"
        await app.at(AsyncDoNothing, my_secret_parameter=value).perform()
        assert expected in caplog.text
