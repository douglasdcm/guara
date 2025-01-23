from guara.transaction import AbstractTransaction


class SubmitTextSelene(AbstractTransaction):
    """
    Submits text using Selene

    Args:
        text (str): The text to be submitted
    """

    def __init__(self, driver):
        super().__init__(driver)

    def do(self, text):
        self._driver.element("#input").type(text)
        self._driver.element("#button").click()
        result = self._driver.element("#result").text
        return result
