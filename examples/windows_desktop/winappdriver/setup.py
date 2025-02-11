from guara.transaction import AbstractTransaction
from appium import webdriver
from appium.options.windows import WindowsOptions


class OpenAppTransaction(AbstractTransaction):
    """Launch Windows Calculator"""

    def __init__(self, driver=None):
        super().__init__(driver)

    def do(self):
        options = WindowsOptions()
        options.set_capability("app", "Microsoft.WindowsCalculator_8wekyb3d8bbwe!App")
        options.set_capability("platformName", "Windows")
        options.set_capability("deviceName", "WindowsPC")

        self._driver = webdriver.Remote(
            command_executor="http://localhost:4723/wd/hub", options=options
        )


class CloseAppTransaction(AbstractTransaction):
    """Close Calculator"""

    def __init__(self, driver):
        super().__init__(driver)

    def do(self):
        self._driver.quit()
