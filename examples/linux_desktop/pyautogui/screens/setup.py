# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

from guara.transaction import AbstractTransaction


class OpenApp(AbstractTransaction):
    """
    Opens the App using dogtail for convenience
    """

    def __init__(self, driver):
        super().__init__(driver)

    def do(self):
        return self._driver


class CloseApp(AbstractTransaction):
    """
    Closes the App using dogtail for convenience
    """

    def do(self):
        from dogtail.procedural import click
        from dogtail.utils import screenshot

        screenshot()
        click("Close")
