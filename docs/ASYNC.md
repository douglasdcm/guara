# Asynchronous execution
Guará is the Python implementation of the design pattern `Page Transactions`. It is more of a programming pattern than a tool. It can be bound to any web driver other than Selenium.

As it can be bound to any Web Driver it can be associated with asynchronous drivers like [Caqui](https://github.com/douglasdcm/caqui). The core of the framework was extended to allow it. The UML diagrams of the asynchronous classes are

<p align="center">
    <img src="https://github.com/douglasdcm/guara/blob/main/docs/images/async/uml_application.png?raw=true" width="800" height="300" />
</p>

Notice the introduction of the `perform` method. It is necessary to run the chain of built-in methods `at` and `asserts`. It calls the list of coroutines. If it is not executed, then the built-in methods are not `waited`.

<p align="center">
    <img src="https://github.com/douglasdcm/guara/blob/main/docs/images/async/uml_abstract_transaction.png?raw=true" width="600" height="300" />
</p>

The built-in classes `OpenApp` and `CloseApp` are here just for compatibility with the synchronous design, but it is not implemented and not bound to any driver. Testers need to choose it by themselves.

<p align="center">
    <img src="https://github.com/douglasdcm/guara/blob/main/docs/images/async/uml_iassertion.png?raw=true" width="800" height="300" />
</p>

There is a subtle change in `asserts` method. In this design the `actual` is an `AbstractTransaction`. Internally the method gets the `AbstractTransaction.result` and compares it against the expected value.

## Examples

```python
from pathlib import Path
from pytest_asyncio import fixture
from pytest import mark
from guara.asynchronous.it import IsEqualTo
from guara.asynchronous.transaction import Application
from examples.web_ui.caqui.asynchronouos.home import GetNthLink
from examples.web_ui.caqui.asynchronouos.setup import OpenApp, CloseApp
from caqui.easy.capabilities import CapabilitiesBuilder
from caqui.synchronous import get_session


class TestAsyncTransaction:
    @fixture(loop_scope="function")
    async def setup_test(self):
        file_path: Path = Path(__file__).parent.parent.parent.parent.resolve()
        self._driver_url: str = "http://127.0.0.1:9999"
        capabilities = (
            CapabilitiesBuilder()
            .browser_name("chrome")
            .accept_insecure_certs(True)
            .additional_capability(
                {"goog:chromeOptions": {"extensions": [], "args": ["--headless"]}}
            )
        ).build()

        self._session = get_session(self._driver_url, capabilities)
        self._app = Application(self._session)
        await self._app.at(
            transaction=OpenApp, with_session=self._session, connect_to_driver=self._driver_url,
            access_url=f"file:///{file_path}/sample.html",
        ).perform()
        yield
        await self._app.at(
            transaction=CloseApp, with_session=self._session, connect_to_driver=self._driver_url,
        ).perform()

    @mark.asyncio
    async def test_async_caqui(self, setup_test):
        await self._app.at(
            transaction=GetNthLink, link_index=1, with_session=self._session, connect_to_driver=self._driver_url,
        ).asserts(IsEqualTo, "any1.com").perform()
```

Check more details [here](https://github.com/douglasdcm/guara/blob/main/examples/web_ui/caqui/asynchronouos/test_async.py)
