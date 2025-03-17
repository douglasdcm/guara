# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

from pytest import mark
from guara.transaction import Application
from guara import it
from examples.web_ui.undetected_chromedriver import setup, actions
from guara.utils import is_dry_run
import undetected_chromedriver as uc


class TestUndetectedChromeDriver:
    def setup_method(self, method):
        driver = None
        if not is_dry_run():
            driver = uc.Chrome(headless=True)
        self._app = Application(driver)
        self._app._driver = self._app.at(setup.OpenBrowserTransaction)._driver

    def teardown_method(self, method):
        self._app.at(setup.CloseBrowserTransaction)

    @mark.parametrize("query", ["Guara framework", "undetected-chromedriver"])
    def test_google_search(self, query):

        self._app.at(actions.SearchGoogle, query=query).asserts(
            it.Contains, "https://www.google.com/search"
        )
