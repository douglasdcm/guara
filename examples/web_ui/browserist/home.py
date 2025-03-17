# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

from guara.transaction import AbstractTransaction


class SubmitText(AbstractTransaction):
    """
    Submits the text

    Args:
        text (str): The text to be submited

    Returns:
        str: the label 'It works! {code}!'
    """

    def do(self, text):
        TEXT = '//*[@id="input"]'
        BUTTON_TEST = '//*[@id="button"]'
        RESULT = '//*[@id="result"]'
        self._driver.input.value(TEXT, text)
        self._driver.click.button(BUTTON_TEST)
        return self._driver.get.text(RESULT)
