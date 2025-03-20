# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

from pathlib import Path
from pytest_asyncio import fixture
from pytest import mark
from typing import Any, Dict, Union, Generator
from guara.asynchronous.it import IsEqualTo
from guara.asynchronous.transaction import Application
from examples.web_ui.caqui.asynchronouos.home import GetNthLink
from examples.web_ui.caqui.asynchronouos.setup import OpenApp, CloseApp


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
        # Lazy import to avoid installation of the library
        from caqui.easy.capabilities import CapabilitiesBuilder
        from caqui.synchronous import get_session

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

        self._session: Any = get_session(self._driver_url, capabilities)
        self._app: Application = Application(self._session)
        await self._app.at(
            transaction=OpenApp,
            with_session=self._session,
            connect_to_driver=self._driver_url,
            access_url=f"file:///{file_path}/sample.html",
        ).perform()
        yield
        await self._app.at(
            transaction=CloseApp,
            with_session=self._session,
            connect_to_driver=self._driver_url,
        ).perform()

    @mark.asyncio
    async def test_async_caqui(self, setup_test) -> None:
        """
        Testing the asynchronuous pages.
        """
        await self._app.at(
            transaction=GetNthLink,
            link_index=1,
            with_session=self._session,
            connect_to_driver=self._driver_url,
        ).asserts(IsEqualTo, "any1.com").perform()
