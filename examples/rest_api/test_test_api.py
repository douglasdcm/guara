from examples.rest_api import echo_api
from guara.transaction import Application
from guara import it


class TestEchoApi:
    def setup_method(self, method):
        self._app = Application(None)

    def test_get_asserts_has_key_value(self):
        path = {"any": "any", "foo1": "bar1s"}
        expected = {"foo1": "bar1s"}
        self._app.at(echo_api.Get, path=path).asserts(it.HasKeyValue, expected)

    def test_get(self):
        expected = {"foo1": "bar1", "foo2": "bar2"}
        self._app.at(echo_api.Get, path=expected).asserts(it.IsEqualTo, expected)

    def test_post(self):
        expected = "This is expected to be sent back as part of response body."
        self._app.at(echo_api.Post, data=expected).asserts(it.IsEqualTo, expected)
