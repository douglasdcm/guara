from guara.transaction import AbstractTransaction


class OpenBrowserTransaction(AbstractTransaction):
    """Open browser using undetected-chromedriver"""

    def __init__(self, driver=None):
        super().__init__(driver)

    def do(self):
        return self._driver  # Return the driver for Guará to manage


class CloseBrowserTransaction(AbstractTransaction):
    """Close the browser safely"""

    def __init__(self, driver):
        super().__init__(driver)

    def do(self):
        self._driver.quit()
