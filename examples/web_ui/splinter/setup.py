from datetime import datetime
from splinter import Browser
from guara.transaction import AbstractTransaction
import os

class OpenSplinterApp(AbstractTransaction):
    """
    Opens the app using Splinter

    Args:
        url (str): the URL to open.
        headless (bool): whether to run the browser in headless mode.
    """

    def __init__(self, driver):
        super().__init__(driver)
        self.browser = driver

    def do(self, url, headless=True):
        self.browser.visit(url)


class CloseSplinterApp(AbstractTransaction):
    """
    Closes the app and saves its screenshot (PNG) using Splinter

    Args:
        screenshot_filename (str): the name of the screenshot file.
        Defaults to './captures/guara-{datetime.now()}.png'.
    """

    def __init__(self, driver):
        super().__init__(driver)
        self.browser = driver

    def do(self, screenshot_filename="./captures/guara-capture"):
        os.makedirs(os.path.dirname(screenshot_filename), exist_ok=True)
        self.browser.screenshot(f"{screenshot_filename}-{datetime.now()}.png")
        self.browser.quit()