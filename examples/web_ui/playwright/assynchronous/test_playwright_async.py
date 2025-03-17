# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

from asyncio import get_event_loop
from pytest import mark
from guara.asynchronous.transaction import Application, AbstractTransaction
from guara.asynchronous import it
from playwright.async_api import async_playwright


class OpenApp(AbstractTransaction):
    async def do(
        self,
        url: str,
        window_width: int = 1094,
        window_height: int = 765,
        timeout: int = 60000,
    ):
        page = self._driver["page"]
        await page.set_viewport_size({"width": window_width, "height": window_height})
        await page.goto(url, timeout=timeout, wait_until="domcontentloaded")
        return await page.title()


class CloseApp(AbstractTransaction):
    async def do(self, screenshot_filename: str = "./captures/guara-capture"):
        page = self._driver["page"]
        browser = self._driver["browser"]
        timestamp = get_event_loop().time()
        await page.screenshot(path=f"{screenshot_filename}-{timestamp:.0f}.png")
        await page.close()
        await browser.close()


class NavigateToDocs(AbstractTransaction):
    async def do(self):
        page = self._driver["page"]
        return await page.text_content("h1")


@mark.asyncio
@mark.skip(
    "Check the requirements to run Playwright in"
    "   https://playwright.dev/python/docs/intro#installing-playwright-pytest"
)
async def test_sample_web_page():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        # Instead of passing just the page it is possible to build a custom `driver`
        # object that hosts the `page` and the `browser`. For example
        # driver = {"browser": browser,
        #           "page": page}
        # Inside of each transaction the page can be accessed by `self._driver["page"]`
        # and the browser can be accessed by `self._driver["browser"]`
        driver = {"browser": browser, "page": page}
        app = Application(driver)

        await app.then(OpenApp, url="https://example.com/").perform()
        await app.when(NavigateToDocs).asserts(it.Contains, "Example Domain").perform()
        await app.then(CloseApp).perform()
