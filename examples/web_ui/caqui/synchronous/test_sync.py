# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

from pytest import mark
from pathlib import Path
from pytest import fixture
from guara.transaction import Application
from guara import it
from examples.web_ui.caqui.synchronous import home, setup
from guara.utils import is_dry_run
from selenium import webdriver


@mark.skipif(not is_dry_run(), reason="Dry run is disabled")
class TestSyncTransaction:
    @fixture(scope="function")
    def setup_test(self):
        file_path = Path(__file__).parent.parent.parent.resolve()
        driver = None
        if not is_dry_run():
            options = webdriver.ChromeOptions()
            options.add_argument("--headless=new")
            driver = webdriver.Chrome(options=options)
        self._app = Application(driver)

        self._app.at(setup.OpenApp, url=f"file:///{file_path}/sample.html")
        yield
        self._app.at(
            setup.CloseApp,
        )

    def test_sync_caqui(self, setup_test):
        """Get all MAX_INDEX links from page and validates its text"""
        self._app.at(home.GetNthLink, link_index=1).asserts(it.IsEqualTo, "any1.com")
