# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

from datetime import datetime
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

    def do(self, url):
        self._driver.get(url)


class CloseAppiumApp(AbstractTransaction):
    """
    Closes the app and saves its screenshot (PNG) using Appium

    Args:
        screenshot_filename (str): the name of the screenshot file.
        Defaults to './captures/guara-{datetime.now()}.png'.
    """

    def __init__(self, driver):
        super().__init__(driver)

    def do(self, screenshot_filename="./captures/guara-capture"):
        """
        Takes a screenshot of the current screen and saves it with a timestamped filename.

        Args:
            screenshot_filename (str): The base filename for the screenshot.
            Defaults to "./captures/guara-capture".

        Returns:
            None
        """
        self._driver.save_screenshot(f"{screenshot_filename}-{datetime.now()}.png")
        self._driver.quit()
