"""
The module that is reponsible for the opening and closing
transactions.
"""

from datetime import datetime
from guara.transaction import AbstractTransaction
from typing import Any


class OpenApp(AbstractTransaction):
    """
    The transaction class for opening an application.
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
        delay: int = 10,
    ) -> str:
        """
        It opens the application and returns its title.

        Args:
            url: (str): The path where the screenshot is saved.
            window_width: (int): The width of the application.
            window_height: (int): The height of the application.
            delay: (int): The implicity timeout for an element to be found.

        Returns:
            (str): the title of the app
        """
        self._driver.set_window_size(window_width, window_height)
        self._driver.get(url)
        self._driver.implicitly_wait(delay)
        return self._driver.title


class CloseApp(AbstractTransaction):
    """
    The transaction class for closing an application.
    """

    def __init__(self, driver: Any):
        """
        Initializing the transaction

        Args:
            driver: (Any): The web driver
        """
        super().__init__(driver)

    def do(self, screenshot_filename: str = "./captures/guara-capture") -> None:
        """
        Closing the application and saving a screenshot.

        Args:
            screenshot_filename: (str): The path where the screenshot is saved.

        Returns:
            (None)
        """
        self._driver.get_screenshot_as_file(f"{screenshot_filename}-{datetime.now()}.png")
        self._driver.quit()
