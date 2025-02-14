from guara.transaction import AbstractTransaction
import undetected_chromedriver as uc


class OpenBrowserTransaction(AbstractTransaction):
    """Open browser using undetected-chromedriver"""

    def __init__(self, driver=None):
        super().__init__(driver)

    def do(self):
        """Configure Chrome options for headless mode"""
        options = uc.ChromeOptions()
        options.add_argument("--headless=new")  # Enable headless mode
        options.add_argument("--disable-gpu")  # Disable GPU for headless
        options.add_argument("--no-sandbox")  # Bypass OS security model (CI/CD)
        options.add_argument("--disable-dev-shm-usage")  # Avoid memory issues in CI/CD

        """Initialize the browser with headless options"""
        self._driver = uc.Chrome(options=options)
        return self._driver  # Return the driver for Guará to manage


class CloseBrowserTransaction(AbstractTransaction):
    """Close the browser safely"""

    def __init__(self, driver):
        super().__init__(driver)

    def do(self):
        self._driver.quit()
