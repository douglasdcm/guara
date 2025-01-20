import pathlib
import random
from splinter import Browser
from guara.transaction import Application
from guara import it
from examples.web_ui.splinter import setup
from examples.web_ui.splinter import home


class TestSplinterIntegration:
    """
    TestSplinterIntegration is a test class for integrating Splinter with a local web page.
    Methods:
    """

    def setup_method(self, method):
        file_path = pathlib.Path(__file__).parent.resolve()
        browser = Browser("chrome", headless=True)
        self._app = Application(browser)
        self._app.at(setup.OpenSplinterApp, url=f"file:///{file_path}/sample.html")

    def teardown_method(self, method):
        self._app.at(setup.CloseSplinterApp)

    def test_local_page(self):
        text = ["cheese", "splinter", "test", "bla", "foo"]
        text = text[random.randrange(len(text))]
        self._app.at(home.SubmitTextSplinter, text=text).asserts(
            it.IsEqualTo, f"It works! {text}!"
        )
        self._app.at(home.SubmitTextSplinter, text=text).asserts(it.IsNotEqualTo, "Any")
