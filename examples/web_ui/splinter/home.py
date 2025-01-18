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

    def __init__(self, driver):
        super().__init__(driver)

    def do(self, text):
        TEXT = '//*[@id="input"]'
        BUTTON_TEST = 'button'
        text_field = self._driver.find_by_id(TEXT).first
        text_field.fill(text)
        button = self._driver.find_by_id(BUTTON_TEST).first
        button.click()
        return "It works!"