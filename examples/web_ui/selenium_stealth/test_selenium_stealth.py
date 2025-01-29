from guara.transaction import Application
from guara import it
from examples.web_ui.selenium_stealth.setup import OpenStealthBrowser, CloseStealthBrowser
from examples.web_ui.selenium_stealth.home import HomeTransactions
from random import randrange


class TestSeleniumStealthIntegration:
    """
    TestSeleniumStealthIntegration is a test class for integrating
    Selenium Stealth with a local web page.
    """

    def setup_method(self, method):
        self._app = Application(None)
        driver = self._app.at(OpenStealthBrowser, headless=True)
        self._app = Application(driver)

    def teardown_method(self, method):
        self._app.at(CloseStealthBrowser)

    def test_local_page(self):
        text = ["cheese", "selenium", "test", "bla", "foo"]
        text = text[randrange(len(text))]
        self._app.at(HomeTransactions, text=text).asserts(
            it.IsEqualTo, f"It works! {text}!"
        )
        self._app.at(HomeTransactions, text=text).asserts(it.IsNotEqualTo, "Any")
