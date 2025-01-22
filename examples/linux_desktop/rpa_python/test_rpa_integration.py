import rpa as r
import pytest
from guara.transaction import Application
from guara import it
from examples.linux_desktop.rpa_python import setup
from examples.linux_desktop.rpa_python import home


@pytest.mark.skip(reason="Complex setup in CI environment")
class TestRPAIntegration:
    """
    TestRPAIntegration is a test class for integrating RPA for Python with a local application.
    """

    def setup_method(self, method):
        self._app = Application(r)
        self._app.at(setup.OpenApplication, app_path="path/to/application.exe")

    def teardown_method(self, method):
        self._app.at(setup.CloseApplication)

    def test_submit_text(self):
        text = "Hello, RPA for Python!"
        self._app.at(home.SubmitTextRPA, text=text).asserts(it.IsEqualTo, text)
