# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

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
        # Instead of passing just the page it is possible to build a custom `driver`
        # object that hosts the `page` and the `browser`. For example
        # driver = {"browser": browser
        #           "page": page}
        # Inside of each transaction the page can be accessed by `self._driver["page"]`
        # and the browser can be accessed by `self._driver["browser"]`
        app = Application(page)

        await app.when(OpenApp, url="https://example.com/").perform()
        await app.when(NavigateToDocs).asserts(it.Contains, "Example Domain").perform()
        await app.when(CloseApp).perform()

        await browser.close()
