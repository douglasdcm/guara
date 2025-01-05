import random
import pytest
import pytest_asyncio
from caqui import synchronous
from caqui.easy.capabilities import CapabilitiesBuilder

# imports from asynchrounous modules
from guara.asynchronous.transaction import Application
from guara.asynchronous import it

from tests.constants import PAGE_URL

# `setup``is not the built-in transaction
from tests.web_ui_async.asynchronouos import setup, home
from tests.web_ui_async.constants import MAX_INDEX


# comment it to execute
# @pytest.mark.skip(
#     reason="before execute it start the driver as a service"
#     "https://github.com/douglasdcm/caqui/tree/main?tab=readme-ov-file#simple-start"
# )
class TestAsyncTransaction:
    # Set the fixtures as asynchronous
    @pytest_asyncio.fixture(loop_scope="function")
    async def setup_test(self):
        # This is how Caqui works
        # https://github.com/douglasdcm/caqui?tab=readme-ov-file#simple-start
        self._driver_url = "http://127.0.0.1:9999"
        capabilities = (
            CapabilitiesBuilder()
            .browser_name("chrome")
            .accept_insecure_certs(True)
            ## comment it to see the UI of the browser
            .additional_capability(
                {"goog:chromeOptions": {"extensions": [], "args": ["--headless"]}}
            )
        ).build()
        self._session = synchronous.get_session(self._driver_url, capabilities)
        self._app = Application(self._session)

        # Notice the introduction of the method `perform`
        # It gets the list of coroutines and exeutes them in order
        await self._app.at(
            setup.OpenApp,
            with_session=self._session,
            connect_to_driver=self._driver_url,
            access_url=PAGE_URL,
        ).asserts(it.IsEqualTo, "Sample page").perform()
        yield
        await self._app.at(
            setup.CloseApp,
            with_session=self._session,
            connect_to_driver=self._driver_url,
        ).perform()

    async def _run_it(self):
        """Get all MAX_INDEX links from page and validates its text"""
        # arrange
        text = ["cheese", "selenium", "test", "bla", "foo"]
        text = text[random.randrange(len(text))]
        expected = []
        max_index = MAX_INDEX - 1
        for i in range(max_index):
            expected.append(f"any{i+1}.com")

        # act and assert
        # the method `perform` runs the coroutine related to GetAllLinks first and saves the
        # result for further asserition. Then, it runs the coroutine of `asserts` and asserts
        # the resuslt against the expected value
        await self._app.at(
            home.GetAllLinks,
            with_session=self._session,
            connect_to_driver=self._driver_url,
        ).asserts(it.IsEqualTo, expected).perform()

        # Does the same think as above, but asserts the items using the built-in method `assert`
        # arrange
        for i in range(max_index):

            # act
            actual = await self._app.at(
                home.GetNthLink,
                link_index=i + 1,
                with_session=self._session,
                connect_to_driver=self._driver_url,
            ).perform()

            # assert
            assert actual.result == f"any{i+1}.com"

    # both tests run in paralell
    # it is necessary to mark the test as async
    @pytest.mark.asyncio
    async def test_async_page_1(self, setup_test):
        await self._run_it()

    @pytest.mark.asyncio
    async def test_async_page_2(self, setup_test):
        await self._run_it()

    @pytest.mark.asyncio
    async def test_async_page_3(self, setup_test):
        await self._run_it()
