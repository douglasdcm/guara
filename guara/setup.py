from datetime import datetime
from guara.transaction import AbstractTransaction


class OpenApp(AbstractTransaction):
    """
    Opens the app

    Args:
        url (str): the path where the screenshot is saved.
        window_width (int): The width of the browser. Defaults to 1094
        window_hight (int): The hight of the browser. Defaults t0 765
        implicitly_wait (int): the implicity timeout for an element to be found.
        Defaults to 10 (seconds)
    Returns:
        str: the title of the app
    """

    def __init__(self, driver):
        super().__init__(driver)

    def do(self, url, window_width=1094, window_hight=765, implicitly_wait=10):
        self._driver.set_window_size(window_width, window_hight)
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

    def __init__(self, driver):
        super().__init__(driver)

    def do(self, screenshot_filename="guara-capture"):
        self._driver.get_screenshot_as_file(
            f"{screenshot_filename}-{datetime.now()}.png"
        )
        self._driver.quit()
