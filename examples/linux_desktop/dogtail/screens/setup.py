# Copyright (C) 2025-2026 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://guara.readthedocs.io/en/latest/

from guara.transaction import AbstractTransaction


class OpenApp(AbstractTransaction):
    """
    Opens the App

    Returns:
        The calculator application
    """

    def do(self):
        return self._driver


class CloseApp(AbstractTransaction):
    """
    Closes the App
    """

    def do(self):
        from dogtail.procedural import click
        from dogtail.utils import screenshot

        screenshot()
        click("Close")
