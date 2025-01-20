import pyautowin
from guara.transaction import AbstractTransaction


class SubmitTextPyAutoWin(AbstractTransaction):
    """
    Submits text using PyAutoWin

    Args:
        text (str): The text to be submitted
    """

    def __init__(self, driver):
        super().__init__(driver)

    def do(self, text):
        pyautowin.typewrite(text)
        pyautowin.press("enter")
