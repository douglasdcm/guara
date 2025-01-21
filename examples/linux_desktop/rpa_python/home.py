import rpa as r
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
        r.type(text)
        r.keyboard("[enter]")