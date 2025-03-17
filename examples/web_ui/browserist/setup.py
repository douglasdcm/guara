# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

from datetime import datetime
from guara.transaction import AbstractTransaction


class OpenApp(AbstractTransaction):
    """
    Opens the app

    Args:
        url (str): the path where the screenshot is saved.
        window_width (int): The width of the browser. Defaults to 1094
        window_height (int): The height of the browser. Defaults t0 765
        implicitly_wait (int): the implicity timeout for an element to be found.
        Defaults to 10 (seconds)
    Returns:
        str: the title of the app
    """

    def do(self, url, window_width=1094, window_height=765, implicitly_wait=10):
        self._driver.window.set.width(window_width)
        self._driver.window.set.height(window_height)
        self._driver.open.url(url)
        self._driver.wait.seconds(implicitly_wait)
        return self._driver.get.page_title()


class CloseApp(AbstractTransaction):
    """
    Closes the app and saves its screenshot (PNG)

    Args:
        screenshot_filename (str): the name of the screenshot file.
        Defaults to 'guara-{datetime.now()}.png'.

        screenshot_destination (str): the path where the screenshot is saved.
        Defaults to './captures'.

    """

    def do(
        self,
        screenshot_destination="./captures",
        screenshot_filename="guara-capture",
    ):
        self._driver.screenshot.complete_page(
            f"{screenshot_filename}-{datetime.now()}.png", screenshot_destination
        )
        self._driver.quit()
