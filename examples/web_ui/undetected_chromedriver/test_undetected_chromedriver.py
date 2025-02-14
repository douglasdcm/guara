import pytest
from guara.transaction import Application
from guara import it
from examples.web_ui.undetected_chromedriver import setup, actions


class TestUndetectedChromeDriver:
    def setup_method(self, method):
        """Initialize the browser"""
        self._app = Application()
        self._app._driver = self._app.at(setup.OpenBrowserTransaction)._driver

    def teardown_method(self, method):
        """Close the browser"""
        self._app.at(setup.CloseBrowserTransaction, driver=self._app._driver)

    @pytest.mark.parametrize("query", ["Guara framework", "undetected-chromedriver"])
    def test_google_search(self, query):
        """Test Google search functionality"""
        self._app.at(actions.SearchGoogle, query=query).asserts(
            it.Contains, "https://www.google.com/search"
        )
