import pytest
from guara.transaction import Application
from guara import it


class TestUndetectedChromeDriver:
    def setup_method(self, method):
        """Lazy import to avoid breaking the pipeline"""
        from examples.web_ui.undetected_chromedriver import setup

        self._app = Application()
        self._app._driver = self.app.at(setup.OpenBrowserTransaction)._driver

    def teardown_method(self, method):
        """Lazy import to avoid breaking the pipeline"""
        from examples.web_ui.undetected_chromedriver import setup

        self._app.at(setup.CloseBrowserTransaction, driver=self._app._driver)

    @pytest.mark.parametrize("query", ["Guara framework", "undetected-chromedriver"])
    def test_google_search(self, query):
        from examples.web_ui.undetected_chromedriver import actions

        self._app.at(actions.SearchGoogle, query=query).asserts(
            it.Contains, "https://www.google.com/search"
        )
