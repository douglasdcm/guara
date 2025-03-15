import pytest
import undetected_chromedriver as uc
from guara.transaction import Application
from guara import it
from examples.web_ui.undetected_chromedriver import setup, actions


class TestUndetectedChromeDriver:
    def setup_method(self, method):
        self._app = Application(uc.Chrome(headless=True))
        self._app._driver = self._app.at(setup.OpenBrowserTransaction)._driver

    def teardown_method(self, method):
        self._app.at(setup.CloseBrowserTransaction)

    @pytest.mark.parametrize("query", ["Guara framework", "undetected-chromedriver"])
    def test_google_search(self, query):

        self._app.at(actions.SearchGoogle, query=query).asserts(
            it.Contains, "https://www.google.com/search"
        )
