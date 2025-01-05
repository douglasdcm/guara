import random
import pytest
from selenium import webdriver

from guara.transaction import Application
from guara import it, setup

from tests.constants import PAGE_URL

# `setup` is not the built-in transaction
from tests.web_ui_async.synchronous import home


# comment it to execute
# @pytest.mark.skip(
#     reason="before execute it start the driver as a service"
#     "https://github.com/douglasdcm/caqui/tree/main?tab=readme-ov-file#simple-start"
# )
class TestSyncTransaction:
    # Set the fixtures as asynchronous
    @pytest.fixture(scope="function")
    def setup_test(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        self._app = Application(webdriver.Chrome(options=options))

        self._app.at(
            setup.OpenApp,
            url=PAGE_URL,
        ).asserts(it.IsEqualTo, "Sample page")
        yield
        self._app.at(
            setup.CloseApp,
        )

    def _run_it(self):
        # arrange
        text = ["cheese", "selenium", "test", "bla", "foo"]
        text = text[random.randrange(len(text))]

        # act and assert
        self._app.at(
            home.GetAllLinks,
        ).asserts(it.IsEqualTo, ["any1.com", "any2.com", "any3.com", "any4.com"])

        # Does the same think as above, but asserts the items using the built-in method `assert`
        # arrange
        MAX_INDEX = 4
        for i in range(MAX_INDEX):

            # act
            actual = self._app.at(
                home.GetNthLink,
                link_index=i + 1,
            )

            # assert
            assert actual.result == f"any{i+1}.com"

    # both tests run in paralell
    # it is necessary to mark the test as async
    @pytest.mark.asyncio
    def test_async_page_1(self, setup_test):
        self._run_it()

    @pytest.mark.asyncio
    def test_async_page_2(self, setup_test):
        self._run_it()

    @pytest.mark.asyncio
    def test_async_page_3(self, setup_test):
        self._run_it()
