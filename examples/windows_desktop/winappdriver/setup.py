from guara.transaction import AbstractTransaction
from appium import webdriver
from guara.transaction import Application


class OpenAppTransaction(AbstractTransaction):
    """Launch Windows Calculator"""

    def __init__(self, driver=None):
        super().__init__(driver)

    def do(self):
        desired_caps = {
            "app": "Microsoft.WindowsCalculator_8wekyb3d8bbwe!App",
            "platformName": "Windows",
            "deviceName": "WindowsPC"
            }
        self._driver = webdriver.Remote(
            command_executor='http://127.0.0.1:4723',
            desired_capabilities=desired_caps
        )
        self._application = Application(self._driver)
        return self._driver


class CloseAppTransaction(AbstractTransaction):
    """Close Calculator"""

    def __init__(self, driver):
        super().__init__(driver)

    def do(self):
        self._driver.quit()
