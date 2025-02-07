# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

from random import randrange
from pathlib import Path
from pytest import fixture
from selenium import webdriver

from guara.transaction import Application
from guara import it, setup

from examples.web_ui.caqui_async.constants import MAX_INDEX

# `setup` is not the built-in transaction
from examples.web_ui.caqui_async.synchronous import home


class TestSyncTransaction:
    # Set the fixtures as asynchronous
    @fixture(scope="function")
    def setup_test(self):
        file_path = Path(__file__).parent.parent.parent.resolve()
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        self._app = Application(webdriver.Chrome(options=options))

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
            result = self._app.at(
                home.GetNthLink,
                link_index=i + 1,
            ).result

            # assert
            it.IsEqualTo().asserts(result, f"any{i+1}.com")

    # both tests run in paralell
    # it is necessary to mark the test as async
    def test_sync_page_1(self, setup_test):
        self._run_it()

    def test_sync_page_2(self, setup_test):
        self._run_it()

    def test_sync_page_3(self, setup_test):
        self._run_it()
