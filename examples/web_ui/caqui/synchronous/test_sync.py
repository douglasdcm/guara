# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

from pytest import mark
from random import randrange
from pathlib import Path
from pytest import fixture
from guara.transaction import Application
from guara import it
from examples.web_ui.caqui.constants import MAX_INDEX
from examples.web_ui.caqui.synchronous import home, setup
from guara.utils import is_dry_run
from selenium import webdriver


@mark.skipif(not is_dry_run(), reason="Dry run is disabled")
class TestSyncTransaction:
    # Set the fixtures as asynchronous
    @fixture(scope="function")
    def setup_test(self):
        file_path = Path(__file__).parent.parent.parent.resolve()
        driver = None
        if not is_dry_run():
            options = webdriver.ChromeOptions()
            options.add_argument("--headless=new")
            driver = webdriver.Chrome(options=options)
        self._app = Application(driver)

        self._app.at(
            setup.OpenApp,
            url=f"file:///{file_path}/sample.html",
        ).asserts(it.IsEqualTo, "Sample page")
        yield
        self._app.at(
            setup.CloseApp,
        )

    def _run_it(self):
        """Get all MAX_INDEX links from page and validates its text"""
        # arrange
        text = ["cheese", "selenium", "test", "bla", "foo"]
        text = text[randrange(len(text))]
        expected = []
        max_index = MAX_INDEX - 1
        for i in range(max_index):
            expected.append(f"any{i+1}.com")

        # act and assert
        self._app.at(
            home.GetAllLinks,
        ).asserts(it.IsEqualTo, expected)

        # Does the same think as above, but asserts the items using the built-in method `assert`
        # arrange
        for i in range(max_index):

            # act
            self._app.at(
                home.GetNthLink,
                link_index=i + 1,
            ).asserts(it.IsEqualTo, f"any{i+1}.com")

    # both tests run in paralell
    # it is necessary to mark the test as async
    def test_sync_page_1(self, setup_test):
        self._run_it()

    def test_sync_page_2(self, setup_test):
        self._run_it()

    def test_sync_page_3(self, setup_test):
        self._run_it()
