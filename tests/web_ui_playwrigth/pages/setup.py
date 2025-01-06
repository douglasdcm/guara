from guara.transaction import AbstractTransaction


class OpenApp(AbstractTransaction):
    """
    Opens the App

    Args:
        with_url (str): The URL of the App

    Returns:
        str: the title of the App
    """

    def __init__(self, driver):
        super().__init__(driver)

    def do(self, with_url):
        self._driver.goto(with_url)
        return self._driver.title()
