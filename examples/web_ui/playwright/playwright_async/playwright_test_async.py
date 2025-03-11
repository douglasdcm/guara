import asyncio
from playwright.async_api import async_playwright
from guara.transaction import Application, AbstractTransaction
from guara import it
import pytest

# Setup transaction to Open the app
class OpenApp(AbstractTransaction):
    async def do(self, url: str, window_width: int = 1094, window_height: int = 765, timeout: int = 60000, **kwargs):
        page = self._driver
        await page.set_viewport_size({"width": window_width, "height": window_height})
        await page.goto(url, timeout=timeout, wait_until="domcontentloaded")
        return await page.title()

# Setup transaction to Close the app
class CloseApp(AbstractTransaction):
    async def do(self, screenshot_filename: str = "./captures/guara-capture", **kwargs):
        page = self._driver
        timestamp = asyncio.get_event_loop().time()
        await page.screenshot(path=f"{screenshot_filename}-{timestamp:.0f}.png")
        await page.close()

# Test transaction to Get page heading
class NavigateToDocs(AbstractTransaction):
    async def do(self, **kwargs):
        page = self._driver
        return await page.text_content("h1")

@pytest.mark.asyncio
async def test_sample_web_page():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        app = Application(page)

        # Open the app
        await app.at(OpenApp, url="https://example.com/")

        # Navigate and assert
        executor = await app.at(NavigateToDocs)
        executor.asserts(it.Contains, "Example Domain")

        # Close the app
        await app.at(CloseApp)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(test_sample_web_page())