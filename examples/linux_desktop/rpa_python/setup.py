import rpa as r
from guara.transaction import AbstractTransaction


class OpenApplication(AbstractTransaction):
    """
    Opens an application using RPA for Python

    Args:
        app_path (str): the path to the application executable.
    """

    def __init__(self, driver):
        super().__init__(driver)

    def do(self, app_path):
        r.init()
        r.run(app_path)


class CloseApplication(AbstractTransaction):
    """
    Closes an application using RPA for Python

    Args:
        app_name (str): the name of the application window.
    """

    def __init__(self, driver):
        super().__init__(driver)

    def do(self, app_name):
        r.close(app_name)
        r.close()