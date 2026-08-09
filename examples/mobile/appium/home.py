# Copyright (C) 2025-2026 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://guara.readthedocs.io/en/latest/

from guara.transaction import AbstractTransaction


class SubmitTextAppium(AbstractTransaction):
    """
    Submits the text using Appium

    Args:
        text (str): The text to be submitted

    Returns:
        str: the label 'It works! {code}!'
    """

    def do(self, text):
        TEXT = '//*[@id="input"]'
        BUTTON_TEST = "button"
        text_field = self._driver.find_element_by_xpath(TEXT)
        text_field.send_keys(text)
        button = self._driver.find_element_by_id(BUTTON_TEST)
        button.click()
        return "It works!"
