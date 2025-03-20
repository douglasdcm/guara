from pathlib import Path
from pytest import mark
from guara.asynchronous.transaction import Application, AbstractTransaction
from guara.asynchronous.it import IsEqualTo


class OpenSamplePage(AbstractTransaction):
    async def do(self, with_url):
        await self._driver.get(with_url)
        element = await self._driver.wait_for_element(5, "h1")
        return await element.get_text()


class Submit(AbstractTransaction):
    async def do(self, text):
        input_box = await self._driver.wait_for_element(5, "#input")
        await input_box.send_keys(text)
        button = await self._driver.wait_for_element(5, "#button")
        await button.click()
        element = await self._driver.wait_for_element(5, "#result")
        return await element.get_text()


@mark.asyncio
@mark.skip(
    reason=(
        "The headless option does not work"
        "refers to https://arsenic.readthedocs.io/en/latest/reference/"
        "supported-browsers.html?highlight=browsers#headless-firefox"
    )
)
async def test_arsenic():
    # Lazy import to avoid installation the library
    from arsenic import get_session, browsers, services

    file_path = Path(__file__).parent.parent.resolve()
    driver_file_path = Path(__file__).parent.resolve()
    URL = f"file:///{file_path}/sample.html"
    GECKODRIVER = f"{driver_file_path}/geckodriver"
    service = services.Geckodriver(binary=GECKODRIVER)
    browser = browsers.Firefox()

    async with get_session(service, browser) as session:
        TEXT = "guara"
        app = Application(session)
        await app.when(OpenSamplePage, with_url=URL).asserts(IsEqualTo, "Basic Page").perform()
        await app.then(Submit, text=TEXT).asserts(IsEqualTo, f"It works! {TEXT}!").perform()
