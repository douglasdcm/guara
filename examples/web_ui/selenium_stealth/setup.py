from guara.transaction import AbstractTransaction
from selenium import webdriver
from selenium_stealth import stealth


class OpenStealthBrowser(AbstractTransaction):
    """Initialize stealth browser"""

    def do(self, headless: bool = True):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--disable-blink-features=AutomationControlled")

        self._driver = webdriver.Chrome(options=options)
        stealth(
            self._driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            fix_hairline=True,
        )
        return self._driver

class CloseStealthBrowser(AbstractTransaction):
    """Close stealth browser"""
    def __init__(self, driver):
        super().__init__(driver)

    def do(self):
        if self._driver:
            self._driver.quit()
