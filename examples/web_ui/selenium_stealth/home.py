from guara.transaction import AbstractTransaction


class SubmitSeleniumStealth(AbstractTransaction):
    """Actions on the home page"""

    def do(self, text):
        self._driver.get("https://example.com")
        search_box = self._driver.find_element("name", "q")
        search_box.send_keys(text)
        search_box.submit()
        return self._driver.page_source
