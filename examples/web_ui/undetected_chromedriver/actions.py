from guara.transaction import AbstractTransaction
from selenium.webdriver.common.by import By


class SearchGoogle(AbstractTransaction):
    """Perform a Google search"""

    def __init__(self, driver):
        super().__init__(driver)

    def do(self, query):
        self._driver.get("https://www.google.com")
        search_box = self._driver.find_element(By.NAME, "q")
        search_box.send_keys(query)
        search_box.submit()
