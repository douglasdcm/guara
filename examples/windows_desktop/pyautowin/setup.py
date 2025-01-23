from guara.transaction import AbstractTransaction


class OpenApplication(AbstractTransaction):
    """
    Opens an application using PyAutoWin

    Args:
        app_path (str): the path to the application executable.
    """

    def __init__(self, driver):
        super().__init__(driver)

    def do(self, app_path):
        self._driver.start(app_path)


class CloseApplication(AbstractTransaction):
    """
    Closes an application using PyAutoWin

    Args:
        app_name (str): the name of the application window.
    """

    def __init__(self, driver):
        super().__init__(driver)

    def do(self, app_name):
        self._driver.close(app_name)
