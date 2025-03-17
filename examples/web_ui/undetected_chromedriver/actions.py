# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

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
        return self._driver.current_url
