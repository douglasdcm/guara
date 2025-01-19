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
        RESULT = '//*[@id="result"]'
        text_field = self._driver.find_by_tag(TEXT).first
        text_field.send_keys(text)
        button = self._driver.find_by_tag(BUTTON_TEST).first
        button.click()
        result = self._driver.find_by_id(RESULT).first
        return result.text