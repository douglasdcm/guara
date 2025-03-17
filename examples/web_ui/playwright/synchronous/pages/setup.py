# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

from guara.transaction import AbstractTransaction


class OpenApp(AbstractTransaction):
    """
    Opens the App

    Args:
        with_url (str): The URL of the App

    Returns:
        str: the title of the App
    """

    def do(self, with_url):
        self._driver.goto(with_url)
        return self._driver.title()
