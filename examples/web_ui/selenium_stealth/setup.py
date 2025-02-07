from guara.transaction import AbstractTransaction


class OpenStealthBrowser(AbstractTransaction):
    """Initialize stealth browser"""

    def __init__(self, driver):
        super().__init__(driver)

    def do(self, url, window_width, window_height, implicitly_wait):
        self._driver.get(url)
        self._driver.set_window_size(window_width, window_height)
        self._driver.implicitly_wait(implicitly_wait)


class CloseStealthBrowser(AbstractTransaction):
    """Close stealth browser"""

    def __init__(self, driver):
        super().__init__(driver)

    def do(self):
        self._driver.quit()
