# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

from logging import warning
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
        try:
            from dogtail.procedural import click
            from dogtail.utils import screenshot

            screenshot()
            click("Close")
        except LookupError:
            warning("Close button not found; the application may already be closed.")
