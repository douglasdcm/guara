from guara.transaction import AbstractTransaction
from guara import it


class HomeTransactions(AbstractTransaction):
    """Actions on the home page"""

    def do(self):
        self._driver.get("https://example.com")
        self._driver.find_element("id", "language-switcher").click()
        return self._driver.page_source

    def validate_language(self, content: str):
        """Custom assertion logic"""
        return it.Contains(value=content)
