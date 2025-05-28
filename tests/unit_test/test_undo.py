# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

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


class TestUndo:
    def setup_method(self, method):
        self._app = Application()

    def teardown_method(self, method):
        self._app.undo()

    def test_get(self):
        any = "any"
        expected = "got any"
        self._app.at(Get, any_param=any).asserts(it.IsEqualTo, expected)

    def test_post(self):
        expected = "posted"
        self._app.at(Post).asserts(it.IsEqualTo, expected)

    def test_get_post_are_executed_in_reverse_order(self):
        # This test does not have assetions. It is necessary to cehck the logs
        # tests/unit_test/test_undo.py::TestUndo::test_get_post_are_executed_in_reverse_order
        # 2025-05-28 00:02:15.150 INFO Transaction: test_undo.Get
        # 2025-05-28 00:02:15.150 INFO  any_param: any
        # 2025-05-28 00:02:15.151 INFO Transaction: test_undo.Post
        # 2025-05-28 00:02:15.151 INFO Reverting 'Post' actions
        # 2025-05-28 00:02:15.151 INFO Reverting 'Get' actions

        self._app.at(Get, any_param="any").at(Post)
