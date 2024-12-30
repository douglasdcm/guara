from tests.rest_api import echo_api
from guara.transaction import Application


class TestEchoApi:
    def setup_method(self, method):
        self._app = Application(None)

    def test_get(self):
        expected = {"foo1": "bar1", "foo2": "bar2"}
        actual = self._app.at(echo_api.Get, path=expected).result
        assert actual["args"] == expected

    def test_post(self):
        expected = "This is expected to be sent back as part of response body."
        actual = self._app.at(echo_api.Post, data=expected).result
        assert actual["data"] == expected
