# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

from pathlib import Path
from pytest_asyncio import fixture
from pytest import mark
from typing import Any, Generator
from guara.asynchronous.it import IsEqualTo
from guara.asynchronous.transaction import Application
from examples.web_ui.caqui.asynchronouos.home import GetNthLink
from examples.web_ui.caqui.asynchronouos.setup import OpenApp, CloseApp
from caqui.easy.options import ChromeOptionsBuilder
from caqui.easy.capabilities import ChromeCapabilitiesBuilder
from caqui.synchronous import get_session
from caqui.easy.server import Server
from time import sleep

SERVER_PORT = 9999
SERVER_URL = f"http://localhost:{SERVER_PORT}"
file_path: Path = Path(__file__).parent.parent.parent.resolve()
PAGE_URL = f"file:///{file_path}/sample.html"


@fixture(scope="function")
def setup_server():
    server = Server.get_instance(port=SERVER_PORT)
    server.start()
    yield
    sleep(3)
    server.dispose()


@fixture
def setup_environment(setup_server):
    options = ChromeOptionsBuilder().args(["headless"]).to_dict()
    capabilities = (
        ChromeCapabilitiesBuilder().accept_insecure_certs(True).add_options(options)
    ).to_dict()
    yield capabilities


class TestAsyncTransactionCaqui:
    """
    The test class for asynchronuous transaction.
    """

    @fixture(loop_scope="function")
    async def setup_test(self, setup_environment) -> Generator[None, Any, None]:  # type: ignore
        """
        Setting up the transaction for the test.

        Returns:
            (Generator[None, Any, None])
        """
        capabilities = setup_environment
        self._session: Any = get_session(SERVER_URL, capabilities)
        self._app: Application = Application(self._session)
        await self._app.at(
            transaction=OpenApp,
            with_session=self._session,
            connect_to_driver=SERVER_URL,
            access_url=f"file:///{file_path}/sample.html",
        ).perform()
        yield
        await self._app.at(
            transaction=CloseApp,
            with_session=self._session,
            connect_to_driver=SERVER_URL,
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
            connect_to_driver=SERVER_URL,
        ).asserts(IsEqualTo, "any1.com").perform()
