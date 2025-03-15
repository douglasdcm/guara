import pytest
import undetected_chromedriver as uc
from guara.transaction import Application
from guara import it


class TestUndetectedChromeDriver:
    def setup_method(self, method):
        """Lazy import to avoid breaking the pipeline"""
        from examples.web_ui.undetected_chromedriver import setup

        """Configure Chrome options for headless mode"""
        options = uc.ChromeOptions()
        options.add_argument("--headless=new")  # Enable headless mode
        options.add_argument("--disable-gpu")  # Disable GPU for headless
        options.add_argument("--no-sandbox")  # Bypass OS security model (CI/CD)
        options.add_argument("--disable-dev-shm-usage")  # Avoid memory issues in CI/CD

        """Initialize the browser with headless options"""
        self._driver = uc.Chrome(options=options)
        self._app = Application()
        self._app._driver = self._app.at(setup.OpenBrowserTransaction)._driver

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
