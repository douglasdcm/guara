from datetime import datetime
from appium import webdriver
from guara.transaction import AbstractTransaction


class OpenAppiumApp(AbstractTransaction):
    """
    Opens the app using Appium

    Args:
        url (str): the URL to open.
        headless (bool): whether to run the browser in headless mode.
    """

    def __init__(self, driver):
        super().__init__(driver)

    def do(self, url, headless=True):
        desired_caps = {
            'platformName': 'Android',
            'deviceName': 'emulator-5554',
            'browserName': 'Chrome',
            'chromeOptions': {'args': ['--headless']} if headless else {}
        }
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        self.driver.get(url)


class CloseAppiumApp(AbstractTransaction):
    """
    Closes the app and saves its screenshot (PNG) using Appium

    Args:
        screenshot_filename (str): the name of the screenshot file.
        Defaults to './captures/guara-{datetime.now()}.png'.
    """

    def __init__(self, driver):
        super().__init__(driver)

    def do(
        self,
        screenshot_filename="./captures/guara-capture",
    ):
        self.driver.save_screenshot(f"{screenshot_filename}-{datetime.now()}.png")
        self.driver.quit()