from guara.transaction import AbstractTransaction


class CloseAppTransaction(AbstractTransaction):
    """Close Calculator"""

    def do(self):
        self._driver.quit()
