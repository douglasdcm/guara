"""
The module that is reponsible for the opening and closing
transactions.
"""
from datetime import datetime
from guara.transaction import AbstractTransaction, WebDriver


class OpenApp(AbstractTransaction):
    """
    It is the transaction for opening application.
    """
    def __init__(self, driver: WebDriver):
        """
        Initializing the transaction

        Parameters:
            driver: WebDriver: The web driver
        """
        super().__init__(driver)

    def do(self, url: str, window_width: int = 1094, window_height: int = 765, implicitly_wait: int = 10) -> str:
        """
        It performs a specific transaction

        Parameters:
            url: string: The path of the directory of the screenshots.
            window_width: int: The width of the browser
            window_height: int: The height of the browser
            implicitly_wait: int: The implicity timeout for an element to be found

        Returns:
            string
        """
        self._driver.set_window_size(window_width, window_height)
        self._driver.get(url)
        self._driver.implicitly_wait(implicitly_wait)
        return self._driver.title


class CloseApp(AbstractTransaction):
    """
    It is the transaction for closing application.
    """
    def __init__(self, driver: WebDriver):
        """
        Initializing the transaction

        Parameters:
            driver: WebDriver: The web driver
        """
        super().__init__(driver)

    def do(self, screenshot_filename: str = "./captures/guara-capture") -> None:
        self._driver.get_screenshot_as_file(f"{screenshot_filename}-{datetime.now()}.png")
        self._driver.quit()
