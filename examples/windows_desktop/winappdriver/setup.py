from guara.transaction import AbstractTransaction


class CloseAppTransaction(AbstractTransaction):
    """Close Calculator"""

    def __init__(self, driver):
        super().__init__(driver)

    def do(self):
        self._driver.quit()
