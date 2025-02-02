"""
The module that is reponsible for the opening and closing
transactions.
"""

from datetime import datetime
from guara.transaction import AbstractTransaction
from typing import Any


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

    def __init__(self, driver: Any):
        """
        Initializing the transaction

        Args:
            driver: (Any): The web driver
        """
        super().__init__(driver)

    def do(
        self,
        url: str,
        window_width: int = 1094,
        window_height: int = 765,
        implicitly_wait: int = 10,
    ) -> str:
        self._driver.set_window_size(window_width, window_height)
        self._driver.get(url)
        self._driver.implicitly_wait(implicitly_wait)
        return self._driver.title


class CloseApp(AbstractTransaction):
    """
    Closes the app and saves its screenshot (PNG)

    Args:
        screenshot_filename (str): the path where the screenshot is saved.
        Examples: './myfile', '/path/to/myfile'
        Defaults to 'guara-{datetime.now()}.png'.
    """

    def __init__(self, driver: Any):
        """
        Initializing the transaction

        Args:
            driver: (Any): The web driver
        """
        super().__init__(driver)

    def do(self, screenshot_filename: str = "./captures/guara-capture") -> None:
        self._driver.get_screenshot_as_file(f"{screenshot_filename}-{datetime.now()}.png")
        self._driver.quit()
