import asyncio
from playwright.async_api import async_playwright
from guara.asynchronous.transaction import Application, AbstractTransaction
from guara.asynchronous import it
import pytest


class OpenApp(AbstractTransaction):
    async def do(
        self,
        url: str,
        window_width: int = 1094,
        window_height: int = 765,
        timeout: int = 60000,
    ):
        page = self._driver
        await page.set_viewport_size({"width": window_width, "height": window_height})
        await page.goto(url, timeout=timeout, wait_until="domcontentloaded")
        return await page.title()


class CloseApp(AbstractTransaction):
    async def do(self, screenshot_filename: str = "./captures/guara-capture"):
        page = self._driver
        timestamp = asyncio.get_event_loop().time()
        await page.screenshot(path=f"{screenshot_filename}-{timestamp:.0f}.png")
        await page.close()


class NavigateToDocs(AbstractTransaction):
    async def do(self):
        page = self._driver
        return await page.text_content("h1")


@pytest.mark.asyncio
async def test_sample_web_page():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        app = Application(page)

        await app.when(OpenApp, url="https://example.com/").perform()
        await app.when(NavigateToDocs).asserts(it.Contains, "Example Domain").perform()
        await app.when(CloseApp).perform()

        # As playwrite is async, we need to close the browser
        # then it is an exception to Page Transations pattern
        await browser.close()
