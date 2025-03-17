# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

from datetime import datetime
from guara.transaction import AbstractTransaction
from os import makedirs


class OpenSplinterApp(AbstractTransaction):
    """
    Opens the app using Splinter

    Args:
        url (str): the URL to open.
        headless (bool): whether to run the browser in headless mode.
    """

    def do(self, url, headless=True):
        self._driver.visit(url)


class CloseSplinterApp(AbstractTransaction):
    """
    Closes the app and saves its screenshot (PNG) using Splinter

    Args:
        screenshot_filename (str): the name of the screenshot file.
        Defaults to './captures/guara-{datetime.now()}.png'.
    """

    def do(self, screenshot_filename="./captures/guara-capture"):
        makedirs("/tmp/captures", exist_ok=True)
        self._driver.screenshot(f"{screenshot_filename}-{datetime.now()}.png")
        self._driver.quit()
