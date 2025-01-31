from guara.transaction import AbstractTransaction
from selenium import webdriver
from selenium_stealth import stealth


class OpenStealthBrowser(AbstractTransaction):
    """Initialize stealth browser"""
    def __init__(self, driver=None):
        super().__init__(driver)

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
        if not self._driver:
            raise RuntimeError("WebDriver instance is not set. Cannot close the browser.")
        self._driver.quit()
