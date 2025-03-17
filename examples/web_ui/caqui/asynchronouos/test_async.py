# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

from time import sleep
from pathlib import Path
from caqui.easy.capabilities import CapabilitiesBuilder
from pytest_asyncio import fixture
from pytest import mark
from typing import Any, Dict, Union, Generator
from caqui.synchronous import get_session
from guara.asynchronous.it import IsEqualTo
from guara.asynchronous.transaction import Application
from examples.web_ui.caqui.asynchronouos.home import GetAllLinks, GetNthLink
from examples.web_ui.caqui.constants import MAX_INDEX
from logging import getLogger, Logger
from examples.web_ui.caqui.asynchronouos.setup import OpenApp, CloseApp


LOGGER: Logger = getLogger(__name__)


@mark.skip(
    reason="before execute it start the driver as a service"
    "https://github.com/douglasdcm/caqui/tree/main?tab=readme-ov-file#simple-start"
)
class TestAsyncTransaction:
    """
    The test class for asynchronuous transaction.
    """

    @fixture(loop_scope="function")
    async def setup_test(self) -> Generator[None, Any, None]:  # type: ignore
        """
        Setting up the transaction for the test.

        Returns:
            (Generator[None, Any, None])
        """
        maximum_attempts: int = 5
        file_path: Path = Path(__file__).parent.parent.parent.parent.resolve()
        self._driver_url: str = "http://127.0.0.1:9999"
        capabilities: Dict[str, Dict[Union[Any, str], Any]] = (
            CapabilitiesBuilder()
            .browser_name("chrome")
            .accept_insecure_certs(True)
            .additional_capability(
                {"goog:chromeOptions": {"extensions": [], "args": ["--headless"]}}
            )
        ).build()
        for index in range(0, maximum_attempts, 1):
            try:
                self._session: Any = get_session(self._driver_url, capabilities)
                LOGGER.debug(f"The session has been retrieved!\nAttempt: {index + 1}")
                break
            except Exception as error:
                LOGGER.warning(
                    f"Failed to retrieve the session.\nAttempt: {index + 1}\nError: {error}"
                )
                sleep(2) if index < maximum_attempts - 1 else None
        else:
            raise RuntimeError("Failed to initialize session after five attempts!")
        self._app: Application = Application(self._session)
        try:
            await self._app.at(
                transaction=OpenApp,
                with_session=self._session,
                connect_to_driver=self._driver_url,
                access_url=f"file:///{file_path}/sample.html",
            ).asserts(IsEqualTo, "Sample page").perform()
        except Exception as error:
            LOGGER.error(f"Failed to open application!\nError: {str(error)}")
            raise
        yield
        try:
            await self._app.at(
                transaction=CloseApp,
                with_session=self._session,
                connect_to_driver=self._driver_url,
            ).perform()
        except Exception as error:
            LOGGER.error(f"Failed to close application!\nError: {str(error)}")
            raise

    async def _run_it(self) -> None:
        """
        Executing the transaction which will iterate over the list
        needed for the test.

        Returns:
            (None)
        """
        max_index: int = MAX_INDEX - 1
        expected = [f"any{index + 1}.com" for index in range(max_index)]
        LOGGER.debug(f"Application: {self._app=}")
        await self._app.at(
            transaction=GetAllLinks,
            with_session=self._session,
            connect_to_driver=self._driver_url,
        ).asserts(IsEqualTo, expected).perform()
        for index in range(max_index):
            iteration: int = index + 1
            actual = await self._app.at(
                transaction=GetNthLink,
                link_index=iteration,
                with_session=self._session,
                connect_to_driver=self._driver_url,
            ).perform()
            assert actual.result == f"any{iteration}.com"

    @mark.asyncio
    async def test_async_page_1(self, setup_test) -> None:
        """
        Testing the asynchronuous pages.

        Returns:
            (None)
        """
        await self._run_it()

    @mark.asyncio
    async def test_async_page_2(self, setup_test) -> None:
        """
        Testing the asynchronuous pages.

        Returns:
            (None)
        """
        await self._run_it()

    @mark.asyncio
    async def test_async_page_3(self, setup_test) -> None:
        """
        Testing the asynchronuous pages.

        Returns:
            (None)
        """
        await self._run_it()

    @mark.asyncio
    async def test_async_page_4(self, setup_test) -> None:
        """
        Testing the asynchronuous pages.

        Returns:
            (None)
        """
        await self._run_it()
