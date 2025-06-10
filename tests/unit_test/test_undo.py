# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

import logging
import pytest
from guara.transaction import Application
from guara import it
from guara.transaction import AbstractTransaction


class Get(AbstractTransaction):
    def do(self, any_param):
        self._any_param = any_param
        return f"got {any_param}"

    def undo(self):
        return f"un-got {self._any_param}"


class Post(AbstractTransaction):
    def do(self):
        return "posted"

    def undo(self):
        return "un-posted"


class Update(AbstractTransaction):
    def do(self):
        return "updated"


class TestUndo:
    @pytest.fixture(autouse=True, scope="function")
    def setup_method(self, caplog):
        caplog.set_level(logging.INFO)
        self._app = Application()
        yield
        self._app.undo()
        assert "Reverting" in caplog.text

    def test_get(self):
        any = "any"
        expected = "got any"
        self._app.at(Get, any_param=any).asserts(it.IsEqualTo, expected)

    def test_post(self):
        expected = "posted"
        self._app.at(Post).asserts(it.IsEqualTo, expected)

    def test_transactions_are_executed_in_reverse_order(self, caplog):
        self._app.at(Get, any_param="any").at(Post).at(Update)
