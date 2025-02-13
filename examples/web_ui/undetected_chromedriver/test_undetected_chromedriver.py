import pytest
from guara.transaction import Application
from guara import it
from examples.web_ui.undetected_chromedriver import setup, actions


class TestUndetectedChromeDriver:
    def setup_method(self):
        """Initialize the browser"""
        self._app = Application()
        self._app.at(setup.OpenBrowserTransaction)

    def teardown_method(self):
        """Close the browser"""
        self._app.at(setup.CloseBrowserTransaction)

    @pytest.mark.parametrize("query", ["Guara framework", "undetected-chromedriver"])
    def test_google_search(self, query):
        """Test Google search functionality"""
        self._app.at(actions.SearchGoogle, query=query).asserts(
            it.Contains, "https://www.google.com/search"
        )
