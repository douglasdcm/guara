from guara.transaction import AbstractTransaction


class OpenSeleneApp(AbstractTransaction):
    """
    Opens the app using Selene

    Args:
        url (str): the URL to open.
    """

    def __init__(self, driver):
        super().__init__(driver)

    def do(self, url):
        self._driver.open(url)


class CloseSeleneApp(AbstractTransaction):
    """
    Closes the app using Selene
    """

    def __init__(self, driver):
        super().__init__(driver)

    def do(self):
        self._driver.quit()
