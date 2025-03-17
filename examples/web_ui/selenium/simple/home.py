# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

from guara.transaction import AbstractTransaction
from selenium.webdriver.common.by import By


class SubmitText(AbstractTransaction):
    """
    Submits the text

    Args:
        text (str): The text to be submited

    Returns:
        str: the label 'It works! {code}!'
    """

    def __init__(self, driver):
        super().__init__(driver)

    def do(self, text):
        text_box = self._driver.find_element(by=By.ID, value="input")
        submit_button = self._driver.find_element(by=By.CSS_SELECTOR, value="button")
        text_box.send_keys(text)
        submit_button.click()
        message = self._driver.find_element(by=By.ID, value="result")
        return message.text
