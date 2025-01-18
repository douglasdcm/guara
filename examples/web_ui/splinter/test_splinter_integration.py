import pathlib
import random
import pytest
from splinter import Browser
from guara.transaction import Application
from guara import it
from .setup import OpenSplinterApp, CloseSplinterApp
from .home import SubmitTextSplinter

# @pytest.mark.skip(reason="Complex setup in CI environment")
class TestSplinterIntegration:
    """
    TestSplinterIntegration is a test class for integrating Splinter with a local web page.
    Methods:
        setup_method(method):
            Sets up the test environment by initializing the browser and application, and opening the sample HTML page.
        teardown_method(method):
            Cleans up the test environment by closing the application.
        test_local_page():
            Tests the local HTML page by submitting text and asserting the expected output.
    """
    def setup_method(self, method):
        file_path = pathlib.Path(__file__).parent.resolve()
        self.browser = Browser('chrome', headless=True)
        self._app = Application(self.browser)
        self._app.at(OpenSplinterApp, url=f"file:///{file_path}/sample.html")


    def teardown_method(self, method):
        self._app.at(CloseSplinterApp)

    def test_local_page(self):
        text = ["cheese", "splinter", "test", "bla", "foo"]
        text = text[random.randrange(len(text))]
        self._app.at(SubmitTextSplinter, text=text).asserts(
            it.IsEqualTo, f"It works! {text}!"
        )
        self._app.at(SubmitTextSplinter, text=text).asserts(it.IsNotEqualTo, "Any")