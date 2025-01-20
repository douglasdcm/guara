import pyautowin
from guara.transaction import Application
from guara import it
from examples.linux_desktop.pyautowin import setup
from examples.linux_desktop.pyautowin import home

class TestPyAutoWinIntegration:
    """
    TestPyAutoWinIntegration is a test class for integrating PyAutoWin with a local application.
    Methods:
    """

    def setup_method(self, method):
        self._app = Application(pyautowin)
        self._app.at(setup.OpenApplication, app_path="path/to/application.exe")

    def teardown_method(self, method):
        self._app.at(setup.CloseApplication, app_name="Application Name")

    def test_submit_text(self):
        text = "Hello, PyAutoWin!"
        self._app.at(home.SubmitTextPyAutoWin, text=text).asserts(
            it.IsEqualTo, text
        )