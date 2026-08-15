# Copyright (C) 2025-2026 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://guara.readthedocs.io/en/latest/

from guara.transaction import AbstractTransaction


class SubmitTextRPA(AbstractTransaction):
    """
    Submits text using RPA for Python

    Args:
        text (str): The text to be submitted
    """

    def do(self, text):
        self._driver.init()
        self._driver.type(text)
        self._driver.keyboard("[enter]")
