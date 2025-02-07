# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

from guara.transaction import AbstractTransaction


class SubmitTextRPA(AbstractTransaction):
    """
    Submits text using RPA for Python

    Args:
        text (str): The text to be submitted
    """

    def __init__(self, driver):
        super().__init__(driver)

    def do(self, text):
        self._driver.init()
        self._driver.type(text)
        self._driver.keyboard("[enter]")
