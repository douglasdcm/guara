import random
import pytest
from caqui import synchronous
from caqui.easy.capabilities import CapabilitiesBuilder
from guara.transaction import Application
from guara import it
from tests.constants import PAGE_URL

# `setup`` is not the built-in transaction
from tests.web_ui_async import setup, home


# comment it to execute
@pytest.mark.skip(
    reason="before execute it start the driver as a service"
    "https://github.com/douglasdcm/caqui/tree/main?tab=readme-ov-file#simple-start"
)
class TestAsyncTransaction:
    def setup_method(self, method):
        # This is how Caqui works
        # https://github.com/douglasdcm/caqui?tab=readme-ov-file#simple-start
        self._driver_url = "http://127.0.0.1:9999"
        capabilities = (
            CapabilitiesBuilder()
            .browser_name("chrome")
            .accept_insecure_certs(True)
            # comment it to see the UI of the browser
            .additional_capability(
                {"goog:chromeOptions": {"extensions": [], "args": ["--headless"]}}
            )
        ).build()
        self._session = synchronous.get_session(self._driver_url, capabilities)
        self._app = Application(self._session)
        self._app.at(
            setup.OpenApp,
            with_session=self._session,
            connect_to_driver=self._driver_url,
            access_url=PAGE_URL,
        )

    def teardown_method(self, method):
        self._app.at(
            setup.CloseApp,
            with_session=self._session,
            connect_to_driver=self._driver_url,
        )

    def _run_it(self):
        # arrange
        text = ["cheese", "selenium", "test", "bla", "foo"]
        text = text[random.randrange(len(text))]

        # act and assert
        self._app.at(
            home.GetAllLinks,
            with_session=self._session,
            connect_to_driver=self._driver_url,
        ).asserts(it.IsEqualTo, ["any1.com", "any2.com", "any3.com", "any4.com"])

        # Does the same think as above but asserts the items using the built-in methsod `assert`
        # arrange
        MAX_INDEX = 4
        for i in range(MAX_INDEX):

            # act
            actual = self._app.at(
                home.GetNthLink,
                link_index=i + 1,
                with_session=self._session,
                connect_to_driver=self._driver_url,
            ).result

            # assert
            assert actual == f"any{i+1}.com"

    # both tests run in paralell
    def test_async_page_1(self):
        self._run_it()

    def test_async_page_2(self):
        self._run_it()
