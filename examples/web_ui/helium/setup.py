# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

from datetime import datetime
from helium import start_chrome, go_to, get_driver, kill_browser
from guara.transaction import AbstractTransaction


class OpenApp(AbstractTransaction):
    """
    Opens the app

    Args:
        url (str): the path where the screenshot is saved.
    """

    def __init__(self, driver):
        super().__init__(driver)

    def do(self, url, headless=True):
        start_chrome(headless=headless)
        go_to(url)


class CloseApp(AbstractTransaction):
    """
    Closes the app and saves its screenshot (PNG)

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
        get_driver().save_screenshot(f"{screenshot_filename}-{datetime.now()}.png")
        kill_browser()
