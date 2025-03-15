# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

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
        self._driver.init()
        self._driver.run(app_path)


class CloseApplication(AbstractTransaction):
    """
    Closes an application using RPA for Python
    """

    def __init__(self, driver):
        super().__init__(driver)

    def do(self):
        self._driver.close()
