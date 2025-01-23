import pytest
from pathlib import Path
from guara.transaction import Application
from guara import it


@pytest.mark.skip(reason="Complex setup in CI environment")
class TestSeleneIntegration:
    """
    TestSeleneIntegration is a test class for integrating Selene with a local web page.
    """

    def setup_method(self, method):
        """Lazy import to avoid triggering module imports"""
        from selene import browser
        from examples.web_ui.selene import setup

        file_path = Path(__file__).parent.parent.parent.resolve()
        self._app = Application(browser)
        self._app.at(setup.OpenSeleneApp,
                     url=f"file:///{file_path}/sample.html")

    def teardown_method(self, method):
        """Lazy import to avoid triggering module imports"""
        from examples.web_ui.selene import setup

        self._app.at(setup.CloseSeleneApp)

    def test_submit_text(self):
        """Lazy import to avoid triggering module imports"""
        from examples.web_ui.selene import home

        text = "Hello, Selene!"
        self._app.at(home.SubmitTextSelene, text=text).asserts(it.IsEqualTo, text)
