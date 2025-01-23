from pathlib import Path
from random import randrange
from guara.transaction import Application
from guara import it


class TestSeleneIntegration:
    """
    TestSeleneIntegration is a test class for integrating Selene with a local web page.
    """

    def setup_method(self, method):
        """Lazy import to avoid triggering module imports"""
        from selene import browser
        from examples.web_ui.selene import setup

        file_path = Path(__file__).parent.parent.resolve()
        self._app = Application(browser)
        self._app.at(setup.OpenSeleneApp, url=f"file:///{file_path}/sample.html")

    def teardown_method(self, method):
        """Lazy import to avoid triggering module imports"""
        from examples.web_ui.selene import setup

        self._app.at(setup.CloseSeleneApp)

    def test_local_page(self):
        """Lazy import to avoid triggering module imports"""
        from examples.web_ui.selene import home

        text = ["cheese", "selenium", "test", "bla", "foo"]
        text = text[randrange(len(text))]
        self._app.at(home.SubmitTextSelene, text=text).asserts(
            it.IsEqualTo, f"It works! {text}!"
        )
        self._app.at(home.SubmitTextSelene, text=text).asserts(it.IsNotEqualTo, "Any")
