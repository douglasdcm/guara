import pytest
from guara.transaction import Application
from guara import it

@pytest.mark.skip(reason="Complex setup in CI environment")
class TestPyAutoWinIntegration:
    """
    TestPyAutoWinIntegration is a test class for integrating PyAutoWin with a local application.
    """

    def setup_method(self, method):
        """Lazy import to avoid triggering module imports"""
        import pyautowin
        from examples.linux_desktop.pyautowin import setup

        self._app = Application(pyautowin)
        self._app.at(setup.OpenApplication, app_path="path/to/application.exe")

    def teardown_method(self, method):
        """Lazy import to avoid triggering module imports"""
        from examples.linux_desktop.pyautowin import setup

        self._app.at(setup.CloseApplication, app_name="Application Name")

    def test_submit_text(self):
        """Lazy import to avoid triggering module imports"""
        from examples.linux_desktop.pyautowin import home

        text = "Hello, PyAutoWin!"
        self._app.at(home.SubmitTextPyAutoWin, text=text).asserts(it.IsEqualTo, text)