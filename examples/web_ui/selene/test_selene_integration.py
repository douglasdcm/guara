from selene import browser
import pathlib
from guara.transaction import Application
from guara import it
from examples.web_ui.selene import setup
from examples.web_ui.selene import home


class TestSeleneIntegration:
    """
    TestSeleneIntegration is a test class for integrating Selene with a local web page.
    """

    def setup_method(self, method):
        file_path = pathlib.Path(__file__).parent.parent.resolve()
        self._app = Application(browser)
        self._app.at(setup.OpenSeleneApp, url="file:///path/to/sample.html")

    def teardown_method(self, method):
        self._app.at(setup.CloseSeleneApp)

    def test_submit_text(self):
        text = "Hello, Selene!"
        self._app.at(home.SubmitTextSelene, text=text).asserts(it.IsEqualTo, text)