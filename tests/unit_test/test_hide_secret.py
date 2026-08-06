# Copyright (C) 2025-2026 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

import logging

import pytest

from guara.asynchronous.guara import (
    AbstractTransaction as AsyncTransaction,
)
from guara.asynchronous.guara import (
    Application as AsyncApp,
)
from guara.constants import GUARA_DRY_RUN, GUARA_VERBOSE, SECRET_DEFAULT_VALUE
from guara.guara import AbstractTransaction, Application


class DoNothing(AbstractTransaction):
    def do(self, any_param=None, my_secret_parameter=None, my_password=None):
        return


@pytest.mark.skipif(GUARA_VERBOSE is False, reason="GUARA_VERBOSE is not true.")
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
        expected = SECRET_DEFAULT_VALUE
        self._app.at(DoNothing, my_secret_parameter="foo")
        assert expected in caplog.text

    def test_hide_when_parameter_is_password(self, caplog):
        caplog.set_level(logging.INFO)
        expected = SECRET_DEFAULT_VALUE
        self._app.at(DoNothing, my_password="foo")
        assert expected in caplog.text


class AsyncDoNothing(AsyncTransaction):
    async def do(self, any_param=None, my_secret_parameter=None):
        return


@pytest.mark.skipif(
    GUARA_VERBOSE is False or GUARA_DRY_RUN is True, reason="GUARA_VERBOSE is not true"
)
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
        expected = SECRET_DEFAULT_VALUE
        await app.at(AsyncDoNothing, my_secret_parameter=value).perform()
        assert expected in caplog.text
