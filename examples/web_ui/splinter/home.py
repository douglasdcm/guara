from splinter import Browser
from guara.transaction import AbstractTransaction


class SubmitTextSplinter(AbstractTransaction):
    """
    Submits the text using Splinter

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